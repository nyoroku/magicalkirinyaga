from django import template
from tour.models import Trip


def do_holiday_trips(parser, token):
    return HolidayNode()


class HolidayNode(template.Node):
    def render(self, context):
        context['holiday'] = Trip.objects.filter(category__title__exact='Holiday Packages')[:10]
        return ''


register = template.Library()
register.tag('get_holiday_trips', do_holiday_trips)
