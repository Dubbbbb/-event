from django import template
from events.models import Notification

register = template.Library()


@register.simple_tag(takes_context=True)
def notifications_count(context):
    user = context['request'].user
    return user.notification.filter(checked=0).count()