from django import template
from core.models import OrderList

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        query = OrderList.objects.filter(user = user, ordered = False)
        if query.exists():
            return query[0].items.count()
    return 0

