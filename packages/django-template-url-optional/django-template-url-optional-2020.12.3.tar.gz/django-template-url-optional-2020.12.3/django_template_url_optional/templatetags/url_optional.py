#!/usr/bin/env python
from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag
def url_optional(viewname,*args,**kwargs):
    return reverse(viewname,
        args=list(filter(None,args)),
        kwargs={k: v for k, v in kwargs.items() if v}
    )
