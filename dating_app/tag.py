from django import template

register = template.Library()


@register.filter
def unread_messages(user):
    return user.InstantMessage.filter(viewed=False).count()
    #replace the messages_set with the appropriate related_name, and also the filter field. (I am assuming it to be "read")

register.simple_tag(unread_messages)
