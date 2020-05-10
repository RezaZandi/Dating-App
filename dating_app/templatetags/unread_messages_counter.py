from django import template
from dating_app import models 

register = template.Library()

@register.simple_tag
def unread_messages(user):

    return user.receiver.filter(viewed=False).count()
    #replace the messages_set with the appropriate related_name, and also the filter field. (I am assuming it to be "read")


