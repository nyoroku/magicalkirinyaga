from django import template
from home.models import Latest


def do_latest_news(parser, token):
    return LatestNewsNode()


class LatestNewsNode(template.Node):
    def render(self, context):
        context['latest_news'] = Latest.objects.order_by('-created')[:3]
        return ''


register = template.Library()
register.tag('get_latest_news', do_latest_news)
