from django import template
from core.models import Item, OrderedItem, OrderList
from django.db.models import Sum

register = template.Library()

@register.filter(name='inlist')
def if_inlist(x):
    query = OrderedItem.objects.values("item__title").annotate(total_sold=Sum("quantity")).all()
    for obj in query:
        for key, value in obj.items():
            if x == value:
                return obj['total_sold']