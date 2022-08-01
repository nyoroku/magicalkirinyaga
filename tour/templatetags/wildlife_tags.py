from django import template
from tour.models import Trip


def do_wildlife_trips(parser, token):
    return WildlifeNode()


class WildlifeNode(template.Node):
    def render(self, context):
        context['wildlife'] = Trip.objects.filter(category__title__exact='Wildlife adventures')[:10]
        return ''


register = template.Library()
register.tag('get_wildlife_trips', do_wildlife_trips)