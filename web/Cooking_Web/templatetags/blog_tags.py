from django import template
from Cooking_Web.models import Category
from django.db.models import Count, Q

register = template.Library()

@register.simple_tag()
def get_all_categories():
    return Category.objects.annotate(
        cnt=Count('posts', filter=Q(posts__published=True))
    ).filter(cnt__gt=0)

