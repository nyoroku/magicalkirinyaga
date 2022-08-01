from django.conf.urls import url
from . import views
from .views import travel


app_name = 'tour'
urlpatterns = [



    url(r'^travel/', travel, name='travel'),
    url(r'^alltrips/', views.alltrips, name='alltrips'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.alltrips,
          name='alltrips_by_tag'),
    url(r'^trip/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' \
           r'(?P<trip>[-\w]+)/$',
           views.trip_detail,
           name='trip-detail'),

]