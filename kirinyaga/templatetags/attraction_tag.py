from django import template
from kirinyaga.models import Attraction


def do_attractions(parser, token):
    return AttractionNode()


class AttractionNode(template.Node):
    def render(self, context):
        context['attractions'] = Attraction.objects.order_by('-date_added')[:6]
        return ''


register = template.Library()
register.tag('get_attractions', do_attractions)
