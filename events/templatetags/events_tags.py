from django import template
from events.models import Latest


def do_latest_events(parser, token):
    return LatestEventsNode()


class LatestEventsNode(template.Node):
    def render(self, context):
        context['events'] = Latest.objects.order_by('-created')[:3]
        return ''


register = template.Library()
register.tag('get_latest_events', do_latest_events)
