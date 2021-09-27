from ..models import Auction
from django import template

register = template.Library()

@register.simple_tag
def listCategories():
  return Auction.objects.all()