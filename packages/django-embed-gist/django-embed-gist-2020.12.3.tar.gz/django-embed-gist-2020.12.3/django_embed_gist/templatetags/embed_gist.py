#!/usr/bin/env python
from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

"""
{% load embed_gist %}

{{ post.body|embed_gist }}
"""

def repl(m):
    if "https://gist.github.com/" not in m[0]:
        return m[0]
    a = re.compile('<a[^>]* href="([^"]*)"')
    url = a.match(m[0]).group(1)
    gist_id = url.split("/")[-1]
    return """<script src="https://gist.github.com/%s.js"></script>""" % gist_id

@register.filter
def embed_gist(html):
    return re.sub(r'<a.*?>(.+?)</a>', repl, html)
