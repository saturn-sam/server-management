from django import template

register = template.Library()

def active_reply(comment):
    return comment.replies.filter(active=True)

register.filter('active_reply', active_reply)