from django import template
from kirinyaga.models import Attraction, Place


def do_places(parser, token):
    return PlaceNode()


class PlaceNode(template.Node):
    def render(self, context):
        context['places'] = Place.objects.filter(status='published').order_by('-date_added')
        return ''


register = template.Library()
register.tag('get_places', do_places)
