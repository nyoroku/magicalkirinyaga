from django import template
from tour.models import Trip


def do_road_trips(parser, token):
    return RoadTripNode()


class RoadTripNode(template.Node):
    def render(self, context):
        context['roadtrips'] = Trip.objects.filter(category__title__exact='Road Trips')[:10]
        return ''


register = template.Library()
register.tag('get_road_trips', do_road_trips)
