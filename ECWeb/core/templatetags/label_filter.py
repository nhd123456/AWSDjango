from django import template
from core.models import Item, OrderedItem, OrderList
from django.db.models import Sum

register = template.Library()

@register.filter(name='lbf')
def label_filter(item):
    if item.label == 'P':
        return 1
