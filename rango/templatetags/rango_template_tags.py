from django import template
from rango.views import sanitize_categories

register = template.Library()


@register.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):
    cats, pages = sanitize_categories()
    return {'cats': cats, 'active_cat':cat}