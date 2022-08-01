from django import template
from tour.models import Trip


def do_top_trips(parser, token):
    return TopTripNode()


class TopTripNode(template.Node):
    def render(self, context):
        context['top_trips'] = Trip.objects.filter(category__title__exact='Top Destinations').order_by('-date_added')[:10]
        return ''


register = template.Library()
register.tag('get_top_trips', do_top_trips)




