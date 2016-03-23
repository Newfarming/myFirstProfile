# coding: utf-8

from django import template

from Pinbot.settings import STATIC_URL

register = template.Library()


@register.simple_tag(takes_context=True)
def static_inject(context):
    request = context.get('request')
    if request:
        host = request.get_host()
    else:
        host = 'www.pinbot.me'
    email_host = 'http://%s/' % host

    static_url = '%s%s' % (email_host.rstrip('/'), STATIC_URL)
    context['email_host'] = email_host
    context['static_url'] = static_url
    return ''


@register.simple_tag(takes_context=True)
def inject_static(context, request):
    host = 'http://%s' % request.META['HTTP_HOST']
    static_url = '%s%s' % (host, STATIC_URL)
    context['email_host'] = host
    context['static_url'] = static_url
    return ''
