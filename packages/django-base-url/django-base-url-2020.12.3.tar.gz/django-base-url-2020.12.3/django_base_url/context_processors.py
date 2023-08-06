#!/usr/bin/env python
from django.conf import settings

"""
settings.py:
TEMPLATE_CONTEXT_PROCESSORS = (
    "django_base_url.context_processors.base_url",
)

template.html:
{{ BASE_URL }}
"""

def base_url(request):
    """
    Return a BASE_URL template context for the current request.
    """
    if hasattr(settings,"BASE_URL"):
        return {'BASE_URL': settings.BASE_URL}
    scheme = 'https://' if request.is_secure() else 'http://'
    return {'BASE_URL': scheme + request.get_host()}
