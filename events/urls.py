from django.conf.urls import url
from . import views

app_name = 'events'
urlpatterns = [

    url(r'^event/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' 
        r'(?P<event>[-\w]+)/$',
        views.event_detail,
        name='event-detail'),

    url(r'^all_events/', views.all_events, name='allevents'),
    url(r'^add-event/$', views.EventCreateView.as_view(), name='event_add'),
    url(r'^my_events/$', views.ManageEventListView.as_view(), name='my_events'),
    url(r'^(?P<pk>\d+)/event_edit/$', views.EventUpdateView.as_view(), name='event_edit'),
    url(r'^(?P<pk>\d+)/event_delete/$', views.EventDeleteView.as_view(), name='event_delete'),
    url(r'^tags/(?P<tag_slug>[-\w]+)/$', views.all_events,
          name='all_events_by_tag'),
]
