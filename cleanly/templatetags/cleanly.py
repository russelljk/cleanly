from django import template
from cleanly import sanitize_html, cleanup_html, sanitizer_manager, run_sanitizer
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='cleanup_html')
def cleanup_html(html):
    return mark_safe(cleanup_html(html))

@register.filter(name='sanitize_html')
def sanitize_html(html):
    return mark_safe(sanitize_html(html, False))

@register.filter(name='restricted_html')
def restricted_html(html):
    return mark_safe(sanitize_html(html, True))
    
@register.filter(name='clean_with')
def restricted_html(html, sanitizer_name):
    sanitizer = sanitizer_manager.lookup(sanitizer_name)
    return mark_safe(run_sanitizer(html, sanitizer))