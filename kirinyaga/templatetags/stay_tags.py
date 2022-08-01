from django import template
from kirinyaga.models import Stay


def do_stays(parser, token):
    return StayNode()


class StayNode(template.Node):
    def render(self, context):
        context['stays'] = Stay.objects.filter(status='published').order_by('-date_added')
        return ''


register = template.Library()
register.tag('get_stays', do_stays)
