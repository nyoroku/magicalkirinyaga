from django.shortcuts import render, get_object_or_404
from .models import Trip, Image
from taggit.models import Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count


def travel(request):
    return render(request, 'tour/index.html')


def alltrips(request, tag_slug=None):
    trips = Trip.objects.all().order_by('-date_added')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        trips = trips.filter(tags__in=[tag])

    paginator = Paginator(trips, 2)
    page = request.GET.get('page')
    try:
        trips = paginator.page(page)
    except PageNotAnInteger:
        trips = paginator.page(1)
    except EmptyPage:
        trips = paginator.page(paginator.num_pages)
    return render(request, 'tour/trips/alltrips.html', {'trips': trips, 'page': page, 'tag': tag})


def trip_detail(request, year, month, day, trip):
    trip = get_object_or_404(Trip, slug=trip)
    image = Image.objects.filter(trip=trip)
    trip_tag_ids = trip.tags.values_list('id', flat=True)
    similar_trips = Trip.objects.filter(tags__in=trip_tag_ids).exclude(id=trip.id)
    similar_trips = similar_trips.annotate(same_tags=Count('tags')).order_by('-same_tags', '-date_added')[:5]
    return render(request, 'tour/trips/trip_detail.html', {'trip': trip, 'image': image, 'similar_trips': similar_trips})







