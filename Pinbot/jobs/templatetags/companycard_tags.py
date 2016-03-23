# coding: utf-8

from django import template
register = template.Library()

@register.filter
def has_user_guide(user):
    profile = user.get_profile()
    if profile.guide_switch:
        profile.guide_switch = False
        profile.save()
        return True
    else:
        return False

@register.filter   
def show_external_url(url):
    if url.startswith("http"):
        return url
    else:
        return "http://"+url
