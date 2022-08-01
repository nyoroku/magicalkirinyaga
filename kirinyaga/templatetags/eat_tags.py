from django import template
from kirinyaga.models import Eat


def do_eats(parser, token):
    return EatNode()


class EatNode(template.Node):
    def render(self, context):
        context['eats'] = Eat.objects.filter(status='published').order_by('-date_added')
        return ''


register = template.Library()
register.tag('get_eats', do_eats)
