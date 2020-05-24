from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django_resized import ResizedImageField
# Create your models here.

CATEGORY_CHOICE = (
    ('C', 'cosemetic'),
    ('A', 'accessories')
)

LABEL_CHOICE = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('N', 'New')
)


class Item(models.Model):
    title = models.CharField(max_length = 100)
    category = models.CharField(choices = CATEGORY_CHOICE, max_length = 4)
    label = models.CharField(choices = LABEL_CHOICE, max_length = 4)
    price = models.FloatField()
    discount_price = models.FloatField(blank = True, null = True)
    description = models.TextField()
    slug = models.SlugField()
    volume = models.IntegerField(default=1)
    cover_image = models.ImageField(blank=True, null=True)
    display = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_abs_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_abs_add_url(self):
        return reverse("core:Add", kwargs={
            'slug': self.slug
        })

    def get_home_url(self):
        return reverse("core:home")

    def get_cart_url(self):
        return reverse("core:cartlist")

class OrderedItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)
    ordered = models.BooleanField(default = False)

    def __str__(self):
        return '{} * {}'.format(self.item.title, self.quantity)

    def subtotal_price(self):
        return self.item.price * self.quantity

    def subtotal_discount_price(self):
        return self.item.discount_price * self.quantity

    def amount_saved(self):
        return (self.item.price - self.item.discount_price) * self.quantity

    def final_price(self):
        if self.item.discount_price:
            return self.subtotal_discount_price()
        return self.subtotal_price()

    def final_saved(self):
        if self.item.discount_price:
            return self.amount_saved()
        else:
            return 0

class OrderList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    items = models.ManyToManyField(OrderedItem)
    start_date = models.DateTimeField(auto_now_add = True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default = False)
    shipping_info = models.ForeignKey('shippingInfo', on_delete=models.SET_NULL, blank=True, null=True)
    has_coupon = models.ForeignKey('coupon', on_delete=models.SET_NULL, blank=True, null=True)
    list_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

    def total_orig_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.final_price()
        total = round(total, 2)
        return total

    def total_saved(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.final_saved()
        total = round(total, 2)
        return total

    def total_c_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.final_price()
        if self.has_coupon:
            total -= self.has_coupon.saved
        total = round(total, 2)
        return total

class shippingInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    str_adr = models.CharField(max_length=100)
    apt_adr = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class coupon(models.Model):
    code = models.CharField(max_length=15)
    saved = models.FloatField()

    def __str__(self):
        return self.code

class blog_images(models.Model):
    cover = ResizedImageField(size=[900, 600], quality=100)
    description = models.CharField(max_length=100, blank=True, null=True)
    att_item = models.ForeignKey(Item, related_name='blog_img', on_delete=models.SET_NULL, blank=True, null=True)

class intro_images(models.Model):
    intro = ResizedImageField(size=[240, 180], quality=100)
    att_item = models.ForeignKey(Item, related_name='intro_image', on_delete=models.SET_NULL, blank=True, null=True)



