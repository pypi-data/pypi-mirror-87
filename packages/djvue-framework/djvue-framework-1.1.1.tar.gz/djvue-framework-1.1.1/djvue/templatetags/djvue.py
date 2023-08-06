from django import template
from django.conf import settings
from django.templatetags.static import static

from djvue.utils import render_tag

register = template.Library()


@register.simple_tag
def vue_javascript():
    if settings.DEBUG:
        djvue = dict(src='https://cdn.jsdelivr.net/npm/vue/dist/vue.js')
        return render_tag("script", attrs=djvue)
    else:
        djvue = dict(src='https://cdn.jsdelivr.net/npm/vue/dist/vue.min.js')
        return render_tag("script", attrs=djvue)



@register.simple_tag
def vue_currency_javascript():
    djvue = dict(src='https://unpkg.com/vue-currency-filter@3.2.3/dist/vue-currency-filter.iife.js')
    return render_tag("script", attrs=djvue)


@register.simple_tag
def djvue_javascript():
    djvue = dict(src=static('djvue/dist/djvue.umd.js'))
    return render_tag("script", attrs=djvue)


@register.simple_tag
def djvue_css():
    djvue_css = dict(href=static('djvue/dist/djvue.css'), rel="stylesheet")
    return render_tag("link", attrs=djvue_css)
