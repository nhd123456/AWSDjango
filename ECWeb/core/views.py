from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item, OrderedItem, OrderList, shippingInfo, coupon, blog_images
from .forms import checkoutForm, couponForm

import random
import string
# Create your views here.

class homeView(ListView):
    model = Item
    template_name = "home-page.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cv_image'] = blog_images.objects.all()
        context['display_item'] = Item.objects.filter(display=True)
        return context

class itemDetail(DetailView):
    model = Item
    template_name = "product-page.html"

class invoice(View):
    def get(self, *args, **kwargs):
        try:
            order = OrderList.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'invoice.html', context)
        except ObjectDoesNotExist:
            return redirect("/")

class dboard(View):
    def get(self, *args, **kwargs):
        ordered_list = OrderList.objects.get(user=self.request.user, ordered=False)
        context = {
            'object': ordered_list,
        }
        return render(self.request, 'index.html', context)


def listnum_gen():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def send_order(request):
    ordered_list = OrderList.objects.get(user=request.user, ordered=False)
    prev_order = ordered_list.items.all()
    for del_item in prev_order:
        warehouse_get = Item.objects.filter(title=del_item.item.title)[0]
        warehouse_get.volume -= del_item.quantity
        warehouse_get.save()
        del_item.save()
    prev_order.update(ordered=True)
    for item in prev_order:
        item.save()
    ordered_list.ordered = True
    ordered_list.save()
    messages.error(request, "Order Completed!")
    return redirect("core:home")

class cartList(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = OrderList.objects.get(user = self.request.user, ordered = False)
            context = {
                'object': order
            }
            return render(self.request, 'cart_list.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You Do Not Have an Active Order!")
            return redirect("/")

class ViewData(View):
    def get(self, *args, **kwargs):
        ordered_list = OrderedItem.objects.values("item__title").annotate(total_sold=Sum("quantity")).all().order_by('-total_sold')
        item_all = Item.objects.all()
        context = {
            'items': item_all,
            'soldout': ordered_list,
        }
        return render(self.request, 'dv.html', context)

class check(View):
    def get(self, *args, **kwargs):
        form = checkoutForm()
        ordered_list = OrderList.objects.get(user=self.request.user, ordered=False)
        context = {
            'form': form,
            'object': ordered_list,
            'c_form': couponForm()
        }
        return render(self.request, 'checkout-page.html', context)
    def post(self, *args, **kwargs):
        form = checkoutForm(self.request.POST or None)
        ordered_list = OrderList.objects.get(user = self.request.user, ordered=False)
        if form.is_valid():
            str_adr = form.cleaned_data.get('str_adr')
            apt_adr = form.cleaned_data.get('apt_adr')
            country = form.cleaned_data.get('country')
            zip = form.cleaned_data.get('zip')
            set_bill_adr = form.cleaned_data.get('set_bill_adr')
            save = form.cleaned_data.get('save')
            pay = form.cleaned_data.get('pay')
            billing = shippingInfo(
                user = self.request.user,
                str_adr = str_adr,
                apt_adr = apt_adr,
                country = country,
                zip = zip,
            )
            billing.save()
            ordered_list.shipping_info = billing
            ordered_list.list_number = listnum_gen()
            ordered_list.save()
            return redirect('core:invoice')
        else:
            messages.info(self.request, "Cart Information Updated.")
            return redirect('core:check')

@login_required()
def add_cart(request, slug):
    item = get_object_or_404(Item, slug = slug)
    ordered_item, created = OrderedItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
    )
    order_list = OrderList.objects.filter(user = request.user, ordered = False)

    if order_list.exists():
        order = order_list[0]
        if order.items.filter(item__slug = item.slug).exists():
            ordered_item.quantity += 1
            ordered_item.save()
            messages.info(request, "Cart Information Updated.")
        else:
            messages.info(request, "Item Added to Cart!")
            order.items.add(ordered_item)
    else:
        date = timezone.now()
        order = OrderList.objects.create(user = request.user, ordered_date = date)
        order.items.add(ordered_item)
        messages.info(request, "Item Added to Cart!")
    return redirect("core:product", slug = slug)

@login_required()
def remove_cart(request, slug):
    item = get_object_or_404(Item, slug = slug)
    query = OrderList.objects.filter(
        user = request.user,
        ordered = False
    )
    if query.exists():
        ordered = query[0]
        if ordered.items.filter(item__slug = item.slug).exists():
            ordered_item = OrderedItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            ordered.items.remove(ordered_item)
            ordered_item.delete()
            messages.info(request, "Removed Item From Cart.")
            return redirect("core:cartlist")

@login_required()
def add_single(request, slug):
    item = get_object_or_404(Item, slug=slug)
    query = OrderList.objects.filter(
        user=request.user,
        ordered=False
    )
    if query.exists():
        ordered = query[0]
        if ordered.items.filter(item__slug=item.slug).exists():
            ordered_item = OrderedItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            ordered_item.quantity += 1
            ordered_item.save()
            messages.info(request, "Added 1 to Cart.")
            return redirect("core:cartlist")


@login_required()
def remove_single(request, slug):
    item = get_object_or_404(Item, slug = slug)
    query = OrderList.objects.filter(
        user = request.user,
        ordered = False
    )
    if query.exists():
        ordered = query[0]
        if ordered.items.filter(item__slug = item.slug).exists():
            ordered_item = OrderedItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            if ordered_item.quantity > 1:
                ordered_item.quantity -= 1
                ordered_item.save()
                messages.info(request, "Removed 1 From Cart.")
            else:
                ordered.items.remove(ordered_item)
                messages.info(request, "Removed Item From Cart.")
            return redirect("core:cartlist")
        else:
            messages.info(request, "Item Not in Cart!")
            return redirect("core:cartlist")
    else:
        messages.info(request, "No Active Order!")
        return redirect("core:cartlist")

class add_coupon(View):
    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            form = couponForm(self.request.POST or None)
            if form.is_valid():
                try:
                    code = form.cleaned_data.get('code')
                    current_qs = OrderList.objects.get( user = self.request.user, ordered = False)
                    try:
                        code_val = coupon.objects.get(code=code)
                        current_qs.has_coupon = code_val
                        current_qs.save()
                        messages.info(self.request, "Successfully applied coupon!")
                        return redirect('core:check')
                    except ObjectDoesNotExist:
                        messages.warning(self.request, "Not a Valid Coupon!")
                        return redirect('core:check')
                except ObjectDoesNotExist:
                    return redirect('core:check')

def remove_coupon(request):
    user_qs = OrderList.objects.filter(
        user=request.user,
        ordered=False
    )
    if user_qs.exists():
        current_qs = user_qs[0]
        current_qs.has_coupon = None
        current_qs.save()
        messages.warning(request, "Coupon Removed")
        return redirect("core:check")



