from django.shortcuts import render, get_object_or_404, redirect
from taggit.models import Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from .models import Latest
from .forms import EventForm

def event_detail(request, year, month, day, event):
    event = get_object_or_404(Latest, slug=event)
    event_tag_ids = event.tags.values_list('id', flat=True)
    similar_events = Latest.objects.filter(tags__in=event_tag_ids).exclude(id=event.id)
    similar_events = similar_events.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[:3]
    return render(request, 'event/event_detail.html', {'event': event, 'similar_events': similar_events,}

                  )


def all_events(request, tag_slug=None):
    events = Latest.objects.all().order_by('-day')

    order = request.GET.get('order', 'day')
    events = events.order_by(order)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        events = events.filter(tags__in=[tag])

    total_events = events.count()
    paginator = Paginator(events, 24)
    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    return render(request, 'event/all_events.html', {'order': order, 'events': events, 'page': page, 'tag': tag, 'total_events': total_events,
                                                      })


class EventListView(ListView):
    model = Latest
    template_name = 'event/list.html'

    def get_queryset(self):
        qs = super(EventListView, self).get_queryset()
        return qs.filter(provider=self.request.user)


class ProviderMixin(object):
    def get_queryset(self):
        qs = super(ProviderMixin, self).get_queryset()
        return qs.filter(provider=self.request.user)


class ProviderEditMixin(object):
    def form_valid(self, form):
        form.instance.provider = self.request.user
        return super(ProviderEditMixin, form).form_valid(form)


class ProviderEventMixin(ProviderMixin, LoginRequiredMixin):
    model = Latest

    success_url = reverse_lazy('events:my_events')


class ProviderEventEditMixin(ProviderEventMixin, ProviderEditMixin):

    template_name = 'event/create.html'


class ManageEventListView(ProviderEventMixin, ListView):
    template_name = 'event/list.html'
    model = Latest
    context_object_name = 'events'
    paginate_by = 12
    queryset = Latest.objects.all()


@method_decorator([login_required, ], name='dispatch')
class EventCreateView(SuccessMessageMixin, ProviderEventMixin, CreateView, PermissionRequiredMixin):
    model = Latest
    form_class = EventForm
    template_name = 'event/create.html'
    success_message = '%(title)s Successfully Created.'

    def form_valid(self, form):
        form.instance.provider = self.request.user
        return super(EventCreateView, self).form_valid(form)


@method_decorator([login_required,], name='dispatch')
class EventUpdateView(SuccessMessageMixin, ProviderEventMixin, UpdateView, PermissionRequiredMixin):
    template_name = 'event/create.html'
    form_class = EventForm
    success_url = reverse_lazy('events:my_events')
    success_message = '%(title)s Successfully Updated'


@method_decorator([login_required, ], name='dispatch')
class EventDeleteView(SuccessMessageMixin, ProviderEventMixin, DeleteView, PermissionRequiredMixin):
    template_name = 'event/delete.html'
    success_url = reverse_lazy('events:my_events')

    success_message = '%(title)s Successfully Deleted'

