from django import template

register = template.Library()

@register.filter(name='img_get')
def img_get(item_name):
    img = item_name.intro_image.all()
    return img