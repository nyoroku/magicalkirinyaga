from django.conf.urls import url
from . import views


app_name = 'kirinyaga'
urlpatterns = [




    url(r'^attraction/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' \
           r'(?P<attraction>[-\w]+)/$',
           views.attraction_detail,
           name='attraction-detail'),
    url(r'^place/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' \
        r'(?P<place>[-\w]+)/$',
        views.place_detail,
        name='place-detail'),

    url(r'^stay/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' \
        r'(?P<stay>[-\w]+)/$',
        views.stay_detail,
        name='stay-detail'),

    url(r'^eat/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' \
        r'(?P<eat>[-\w]+)/$',
        views.eat_detail,
        name='eat-detail'),
    url(r'^allplaces/', views.all_places, name='allplaces'),
    url(r'^stay/', views.all_stays, name='allstays'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^eat-drink/', views.all_eats, name='alleats'),
    url(r'^my_places/$', views.ManagePlaceListView.as_view(), name='my_list'),
    url(r'^add-place/$', views.PlaceCreateView.as_view(), name='place_add'),
    url(r'^(?P<pk>\d+)/place_edit/$', views.PlaceUpdateView.as_view(), name='place_edit'),
    url(r'^(?P<pk>\d+)/place_delete/$', views.PlaceDeleteView.as_view(), name='place_delete'),
    url(r'^my_accommodations/$', views.ManageStayListView.as_view(), name='my_stays'),
    url(r'^add-accommodation/$', views.StayCreateView.as_view(), name='stay_add'),
    url(r'^(?P<pk>\d+)/accommodation_edit/$', views.StayUpdateView.as_view(), name='stay_edit'),
    url(r'^(?P<pk>\d+)/accommodation_delete/$', views.StayDeleteView.as_view(), name='stay_delete'),
    url(r'^add-eatery/$', views.EatCreateView.as_view(), name='eat_add'),
    url(r'^my_eateries/$', views.ManageEatListView.as_view(), name='my_eats'),
    url(r'^(?P<pk>\d+)/eat_edit/$', views.EatUpdateView.as_view(), name='eat_edit'),
    url(r'^(?P<pk>\d+)/eatery_delete/$', views.EatDeleteView.as_view(), name='eat_delete'),
    url(r'^user_register/$', views.PartnerRegistrationView.as_view(), name='user_registration'),


]