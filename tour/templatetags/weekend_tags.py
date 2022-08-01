from django import template
from tour.models import Trip


def do_weekend_trips(parser, token):
    return WeekendNode()


class WeekendNode(template.Node):
    def render(self, context):
        context['weekend'] = Trip.objects.filter(category__title__exact='Weekend Gateways')[:10]
        return ''


register = template.Library()
register.tag('get_weekend_trips', do_weekend_trips)
