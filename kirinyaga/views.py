from django.shortcuts import render, get_object_or_404, redirect
from .models import Attraction, User, Image, Highlight, Vital, Activity, Facility,Eat, EatImage, Menu, OpeningHours, Place, PlaceImage, Interest, Stay, StayImage, StayFacility, Term, RoomType, InterestingPlace
from taggit.models import Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from .forms import PlaceForm, PartnerRegistrationForm, EatForm, OpeningHoursFormset, EatImageFormSet, EatMenuFormset, PlaceImageFormSet, StayForm, StayTermFormSet, StayInterestFormSet, PlaceActivityFormSet, PlaceFacilityFormSet, PlaceInterestFormSet, StayImageFormSet, StayFacilityFormSet, StayRoomFormSet


def attraction_detail(request, year, month, day, attraction):
    attraction = get_object_or_404(Attraction, slug=attraction)
    image = Image.objects.filter(attraction=attraction)
    highlight = Highlight.objects.filter(attraction=attraction)
    vital = Vital.objects.filter(attraction=attraction)
    attraction_tag_ids = attraction.tags.values_list('id', flat=True)
    similar_attractions = Attraction.objects.filter(tags__in=attraction_tag_ids).exclude(id=attraction.id)
    similar_attractions = similar_attractions.annotate(same_tags=Count('tags')).order_by('-same_tags', '-date_added')[:5]
    return render(request, 'kirinyaga/attraction_detail.html', {'attraction': attraction, 'image': image, 'similar_attractions': similar_attractions,
                                                                'highlight': highlight, 'vital': vital})


def place_detail(request, year, month, day, place):
    place = get_object_or_404(Place, slug=place)
    images = PlaceImage.objects.filter(place=place)[:6]
    interests = Interest.objects.filter(place=place)
    activities = Activity.objects.filter(place=place)
    facilities = Facility.objects.filter(place=place)
    place_tag_ids = place.tags.values_list('id', flat=True)
    similar_place = Place.objects.filter(tags__in=place_tag_ids).exclude(id=place.id)
    similar_place = similar_place.annotate(same_tags=Count('tags')).order_by('-same_tags', '-date_added')[:5]
    return render(request, 'kirinyaga/place_detail.html', {'activities': activities, 'images': images, 'similar_place': similar_place,
                                                                'facilities': facilities, 'place': place,
                                                           'interests': interests})


def stay_detail(request, year, month, day, stay):
    stay = get_object_or_404(Stay, slug=stay)
    rooms = RoomType.objects.filter(stay=stay)
    images = StayImage.objects.filter(stay=stay)[:6]
    interests = InterestingPlace.objects.filter(stay=stay)
    terms = Term.objects.filter(stay=stay)
    facilities = StayFacility.objects.filter(stay=stay)
    stay_tag_ids = stay.tags.values_list('id', flat=True)
    similar_stay = Stay.objects.filter(tags__in=stay_tag_ids).exclude(id=stay.id)
    similar_stay = similar_stay.annotate(same_tags=Count('tags')).order_by('-same_tags', '-date_added')[:5]
    return render(request, 'kirinyaga/stay_detail.html', {'rooms': rooms, 'images': images, 'similar_stay': similar_stay,
                                                                'facilities': facilities, 'stay': stay,
                                                           'interests': interests, 'terms': terms})


def eat_detail(request, year, month, day, eat):
    eat = get_object_or_404(Eat, slug=eat)
    menus = Menu.objects.filter(eat=eat)
    images = EatImage.objects.filter(eat=eat)[:6]
    hours = OpeningHours.objects.filter(eat=eat)
    eat_tag_ids = eat.tags.values_list('id', flat=True)
    similar_eats = Eat.objects.filter(tags__in=eat_tag_ids).exclude(id=eat.id)
    similar_eats = similar_eats.annotate(same_tags=Count('tags')).order_by('-same_tags', '-date_added')[:5]
    return render(request, 'kirinyaga/eat_detail.html', {'menus': menus, 'images': images, 'similar_eats': similar_eats,
                                                                'eat': eat, 'hours': hours
                                                           })


def all_places(request):
    places = Place.objects.filter(status='published').order_by('-date_added')
    order = request.GET.get('order', 'name')
    places = places.order_by(order)
    total_places = places.count()
    paginator = Paginator(places, 20)
    page = request.GET.get('page')
    try:
        places = paginator.page(page)
    except PageNotAnInteger:
        places = paginator.page(1)
    except EmptyPage:
        places = paginator.page(paginator.num_pages)
    return render(request, 'kirinyaga/all_places.html', {'order': order, 'places': places, 'page': page,  'total_places': total_places})


def all_stays(request):
    stays = Stay.objects.filter(status='published').order_by('-date_added')
    order = request.GET.get('order', 'name')
    stays = stays.order_by(order)
    total_stays = stays.count()
    paginator = Paginator(stays, 20)
    page = request.GET.get('page')
    try:
        stays = paginator.page(page)
    except PageNotAnInteger:
        stays = paginator.page(1)
    except EmptyPage:
        stays = paginator.page(paginator.num_pages)
    return render(request, 'kirinyaga/all_stays.html', {'order': order, 'stays': stays, 'page': page,  'total_stays': total_stays})


def all_eats(request):
    places = Eat.objects.filter(status='published').order_by('-date_added')
    order = request.GET.get('order', 'name')
    places = places.order_by(order)
    total_places = places.count()
    paginator = Paginator(places, 20)
    page = request.GET.get('page')
    try:
        places = paginator.page(page)
    except PageNotAnInteger:
        places = paginator.page(1)
    except EmptyPage:
        places = paginator.page(paginator.num_pages)
    return render(request, 'kirinyaga/all_eats.html', {'order': order, 'places': places, 'page': page,  'total_places': total_places})


class PlaceListView(ListView):
    model = Place
    template_name = 'kirinyaga/place_list.html'

    def get_queryset(self):
        qs = super(PlaceListView, self).get_queryset()
        return qs.filter(provider=self.request.user)


class ProviderMixin(object):
    def get_queryset(self):
        qs = super(ProviderMixin, self).get_queryset()
        return qs.filter(provider=self.request.user)


class ProviderEditMixin(object):
    def form_valid(self, form):
        form.instance.provider = self.request.user
        return super(ProviderEditMixin, form).form_valid(form)


class ProviderPlaceMixin(ProviderMixin, LoginRequiredMixin):
    model = Place

    success_url = reverse_lazy('kirinyaga:my_list')


class ProviderPlaceEditMixin(ProviderPlaceMixin, ProviderEditMixin):

    template_name = 'kirinyaga/place_create.html'


class ManagePlaceListView(ProviderPlaceMixin, ListView):
    template_name = 'kirinyaga/place_list.html'
    model = Place
    context_object_name = 'places'
    paginate_by = 12
    queryset = Place.objects.all()


@method_decorator([login_required, ], name='dispatch')
class PlaceCreateView(SuccessMessageMixin, ProviderPlaceMixin, CreateView, PermissionRequiredMixin):
    model = Place
    form_class = PlaceForm
    template_name = 'kirinyaga/place_create.html'
    success_url = reverse_lazy('kirinyaga:my_list')
    success_message = '%(name)s Successfully Created.'

    def get_context_data(self, **kwargs):
        context = super(PlaceCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['placeimages_formset'] = PlaceImageFormSet(self.request.POST, self.request.FILES)
            context['placefacilities_formset'] = PlaceFacilityFormSet(self.request.POST, self.request.FILES)
            context['placeactivities_formset'] = PlaceActivityFormSet(self.request.POST, self.request.FILES)
            context['placeinterests_formset'] = PlaceInterestFormSet(self.request.POST, self.request.FILES)
        else:
            context['placeimages_formset'] = PlaceImageFormSet()
            context['placefacilities_formset'] = PlaceFacilityFormSet()
            context['placeactivities_formset'] = PlaceActivityFormSet()
            context['placeinterests_formset'] = PlaceInterestFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        placeimages_formset = context['placeimages_formset']
        placefacilities_formset = context['placefacilities_formset']
        placeactivities_formset = context['placeactivities_formset']
        placeinterests_formset = context['placeinterests_formset']
        if placeimages_formset.is_valid() and placefacilities_formset.is_valid() and placeactivities_formset.is_valid() and placeinterests_formset.is_valid():
            form.instance.provider = self.request.user
            self.object = form.save()
            placeimages_formset.instance = self.object
            placeimages_formset.save()
            placefacilities_formset.instance = self.object
            placefacilities_formset.save()
            placeactivities_formset.instance = self.object
            placeactivities_formset.save()
            placeinterests_formset.instance = self.object
            placeinterests_formset.save()
            messages.success(self.request, 'New Place Successfully Added')
            return redirect('kirinyaga:my_list')

        else:
            return self.render_to_response(self.get_context_data(form=form))


@method_decorator([login_required, ], name='dispatch')
class PlaceUpdateView(SuccessMessageMixin, ProviderPlaceMixin, UpdateView, PermissionRequiredMixin):
    template_name = 'kirinyaga/place_edit.html'
    success_url = reverse_lazy('kirinyaga:my_list')
    success_message = '%(name)s Successfully Updated'
    model = Place
    form_class = PlaceForm

    def get_context_data(self, **kwargs):
        context = super(PlaceUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['placeimages_formset'] = PlaceImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
            context['placeimages_formset'].full_clean()
            context['placefacilities_formset'] = PlaceFacilityFormSet(self.request.POST, self.request.FILES, instance=self.object)
            context['placefacilities_formset'].full_clean()
            context['placeactivities_formset'] = PlaceActivityFormSet(self.request.POST, self.request.FILES,
                                                                      instance=self.object)
            context['placeactivities_formset'].full_clean()
            context['placeinterests_formset'] = PlaceInterestFormSet(self.request.POST, self.request.FILES,
                                                                      instance=self.object)
            context['placeinterests_formset'].full_clean()

        else:
            context['placeimages_formset'] = PlaceImageFormSet(instance=self.object)
            context['placefacilities_formset'] = PlaceFacilityFormSet(instance=self.object)
            context['placeactivities_formset'] = PlaceActivityFormSet(instance=self.object)
            context['placeinterests_formset'] = PlaceInterestFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        images_formset = context['placeimages_formset']
        facilities_formset = context['placefacilities_formset']
        activities_formset = context['placeactivities_formset']
        interest_formset = context['placeinterests_formset']
        if images_formset.is_valid() and facilities_formset.is_valid() and activities_formset.is_valid() \
                and interest_formset.is_valid():
            response = super(PlaceUpdateView, self).form_valid(form)
            images_formset.instance = self.object
            images_formset.save()
            facilities_formset.instance = self.object
            facilities_formset.save()
            activities_formset.instance = self.object
            activities_formset.save()
            interest_formset.instance = self.object
            interest_formset.save()
            return response
        else:
            return super(PlaceUpdateView, self).form_invalid(form)


@method_decorator([login_required, ], name='dispatch')
class PlaceDeleteView(SuccessMessageMixin, ProviderPlaceMixin, DeleteView, PermissionRequiredMixin):
    template_name = 'kirinyaga/place_delete.html'
    success_url = reverse_lazy('kirinyaga:my_list')

    success_message = 'Successfully Deleted'


class StayListView(ListView):
    model = Stay
    template_name = 'kirinyaga/stay_list.html'

    def get_queryset(self):
        qs = super(StayListView, self).get_queryset()
        return qs.filter(provider=self.request.user)


class SupplierMixin(object):
    def get_queryset(self):
        qs = super(SupplierMixin, self).get_queryset()
        return qs.filter(provider=self.request.user)


class SupplierEditMixin(object):
    def form_valid(self, form):
        form.instance.provider = self.request.user
        return super(SupplierEditMixin, form).form_valid(form)


class SupplierStayMixin(SupplierMixin, LoginRequiredMixin):
    model = Stay

    success_url = reverse_lazy('kirinyaga:my_stays')


class SupplierStayEditMixin(SupplierStayMixin, SupplierEditMixin):

    template_name = 'kirinyaga/stay_create.html'


class ManageStayListView(SupplierStayMixin, ListView):
    template_name = 'kirinyaga/stay_list.html'
    model = Stay
    context_object_name = 'stays'
    paginate_by = 12
    queryset = Stay.objects.all()



@method_decorator([login_required, ], name='dispatch')
class StayCreateView(SuccessMessageMixin, SupplierStayMixin, CreateView, PermissionRequiredMixin):
    model = Stay
    form_class = StayForm
    template_name = 'kirinyaga/stay_create.html'
    success_url = reverse_lazy('kirinyaga:my_stays')
    success_message = '%(name)s Successfully Created.'

    def get_context_data(self, **kwargs):
        context = super(StayCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['stayimages_formset'] = StayImageFormSet(self.request.POST, self.request.FILES)
            context['stayfacilities_formset'] = StayFacilityFormSet(self.request.POST, self.request.FILES)
            context['rooms_formset'] = StayRoomFormSet(self.request.POST, self.request.FILES)
            context['stayinterests_formset'] = StayInterestFormSet(self.request.POST, self.request.FILES)
            context['terms_formset'] = StayTermFormSet(self.request.POST, self.request.FILES)
        else:
            context['stayimages_formset'] = StayImageFormSet()
            context['stayfacilities_formset'] = StayFacilityFormSet()
            context['rooms_formset'] = StayRoomFormSet()
            context['stayinterests_formset'] = StayInterestFormSet()
            context['terms_formset'] = StayTermFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        stayimages_formset = context['stayimages_formset']
        stayfacilities_formset = context['stayfacilities_formset']
        rooms_formset = context['rooms_formset']
        stayinterests_formset = context['stayinterests_formset']
        terms_formset = context['terms_formset']
        if stayimages_formset.is_valid() and stayfacilities_formset.is_valid() and rooms_formset.is_valid() and stayinterests_formset.is_valid() and terms_formset.is_valid():
            form.instance.provider = self.request.user
            self.object = form.save()
            stayimages_formset.instance = self.object
            stayimages_formset.save()
            stayfacilities_formset.instance = self.object
            stayfacilities_formset.save()
            rooms_formset.instance = self.object
            rooms_formset.save()
            stayinterests_formset.instance = self.object
            stayinterests_formset.save()
            terms_formset.instance = self.object
            terms_formset.save()
            messages.success(self.request, 'New Accommodation Successfully Added')
            return redirect('kirinyaga:my_stays')


        else:
            return self.render_to_response(self.get_context_data(form=form))


@method_decorator([login_required, ], name='dispatch')
class StayUpdateView(SuccessMessageMixin, SupplierStayMixin, UpdateView, PermissionRequiredMixin):
    template_name = 'kirinyaga/stay_edit.html'
    success_url = reverse_lazy('kirinyaga:my_stays')
    success_message = '%(name)s Successfully Updated'
    model = Stay
    form_class = StayForm

    def get_context_data(self, **kwargs):
        context = super(StayUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['stayimages_formset'] = StayImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
            context['stayimages_formset'].full_clean()
            context['stayfacilities_formset'] = StayFacilityFormSet(self.request.POST, self.request.FILES, instance=self.object)
            context['stayfacilities_formset'].full_clean()
            context['rooms_formset'] = StayRoomFormSet(self.request.POST, self.request.FILES,
                                                                      instance=self.object)
            context['rooms_formset'].full_clean()
            context['stayinterests_formset'] = StayInterestFormSet(self.request.POST, self.request.FILES,
                                                                      instance=self.object)
            context['stayinterests_formset'].full_clean()
            context['terms_formset'] = StayTermFormSet(self.request.POST, self.request.FILES,
                                                                   instance=self.object)
            context['terms_formset'].full_clean()

        else:
            context['stayimages_formset'] = StayImageFormSet(instance=self.object)
            context['stayfacilities_formset'] = StayFacilityFormSet(instance=self.object)
            context['rooms_formset'] = StayRoomFormSet(instance=self.object)
            context['stayinterests_formset'] = StayInterestFormSet(instance=self.object)
            context['terms_formset'] = StayTermFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        images_formset = context['stayimages_formset']
        facilities_formset = context['stayfacilities_formset']
        rooms_formset = context['rooms_formset']
        interest_formset = context['stayinterests_formset']
        terms_formset = context['terms_formset']
        if images_formset.is_valid() and facilities_formset.is_valid() and rooms_formset.is_valid() \
                and interest_formset.is_valid() and terms_formset.is_valid():
            response = super(StayUpdateView, self).form_valid(form)
            images_formset.instance = self.object
            images_formset.save()
            facilities_formset.instance = self.object
            facilities_formset.save()
            rooms_formset.instance = self.object
            rooms_formset.save()
            interest_formset.instance = self.object
            interest_formset.save()
            terms_formset.instance = self.object
            terms_formset.save()

            return response
        else:
            return super(StayUpdateView, self).form_invalid(form)


@method_decorator([login_required, ], name='dispatch')
class StayDeleteView(SuccessMessageMixin, SupplierStayMixin, DeleteView, PermissionRequiredMixin):
    template_name = 'kirinyaga/stay_delete.html'
    success_url = reverse_lazy('kirinyaga:my_stays')

    success_message = 'Successfully Deleted'


class EatListView(ListView):
    model = Eat
    template_name = 'kirinyaga/stay_list.html'

    def get_queryset(self):
        qs = super(EatListView, self).get_queryset()
        return qs.filter(provider=self.request.user)


class SellerMixin(object):
    def get_queryset(self):
        qs = super(SellerMixin, self).get_queryset()
        return qs.filter(provider=self.request.user)


class SellerEditMixin(object):
    def form_valid(self, form):
        form.instance.provider = self.request.user
        return super(SellerEditMixin, form).form_valid(form)


class SellerEatMixin(SupplierMixin, LoginRequiredMixin):
    model = Eat

    success_url = reverse_lazy('kirinyaga:my_eats')


class SellerEatEditMixin(SellerEatMixin, SellerEditMixin):

    template_name = 'kirinyaga/eat_create.html'


class ManageEatListView(SellerEatMixin, ListView):
    template_name = 'kirinyaga/eat_list.html'
    model = Eat
    context_object_name = 'eats'
    paginate_by = 12
    queryset = Eat.objects.all()



@method_decorator([login_required, ], name='dispatch')
class EatCreateView(SuccessMessageMixin, SellerEatMixin, CreateView, PermissionRequiredMixin):
    model = Eat
    form_class = EatForm
    template_name = 'kirinyaga/eat_create.html'
    success_url = reverse_lazy('kirinyaga:my_eats')
    success_message = '%(name)s Successfully Created.'

    def get_context_data(self, **kwargs):
        context = super(EatCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['eatimages_formset'] = EatImageFormSet(self.request.POST, self.request.FILES)
            context['menu_formset'] = EatMenuFormset(self.request.POST, self.request.FILES)
            context['hours_formset'] = OpeningHoursFormset(self.request.POST, self.request.FILES)

        else:
            context['eatimages_formset'] = EatImageFormSet()
            context['menu_formset'] = EatMenuFormset()
            context['hours_formset'] = OpeningHoursFormset()


        return context

    def form_valid(self, form):
        context = self.get_context_data()
        eatimages_formset = context['eatimages_formset']
        menu_formset = context['menu_formset']
        hours_formset = context['hours_formset']

        if eatimages_formset.is_valid() and menu_formset.is_valid() and hours_formset.is_valid():
            form.instance.provider = self.request.user
            self.object = form.save()
            eatimages_formset.instance = self.object
            eatimages_formset.save()
            menu_formset.instance = self.object
            menu_formset.save()
            hours_formset.instance = self.object
            hours_formset.save()

            messages.success(self.request, 'Successfully Added')
            return redirect('kirinyaga:my_eats')


        else:
            return self.render_to_response(self.get_context_data(form=form))



@method_decorator([login_required, ], name='dispatch')
class EatUpdateView(SuccessMessageMixin, SellerEatMixin, UpdateView, PermissionRequiredMixin):
    template_name = 'kirinyaga/eat_edit.html'
    success_url = reverse_lazy('kirinyaga:my_eats')
    success_message = '%(name)s Successfully Updated'
    model = Eat
    form_class = EatForm

    def get_context_data(self, **kwargs):
        context = super(EatUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['eatimages_formset'] = EatImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
            context['eatimages_formset'].full_clean()
            context['menu_formset'] = EatMenuFormset(self.request.POST, self.request.FILES, instance=self.object)
            context['menu_formset'].full_clean()
            context['hours_formset'] = OpeningHoursFormset(self.request.POST, self.request.FILES,
                                                                      instance=self.object)
            context['hours_formset'].full_clean()


        else:
            context['eatimages_formset'] = EatImageFormSet(instance=self.object)
            context['menu_formset'] = EatMenuFormset(instance=self.object)
            context['hours_formset'] = OpeningHoursFormset(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        images_formset = context['eatimages_formset']
        menu_formset = context['menu_formset']
        hours_formset = context['hours_formset']

        if images_formset.is_valid() and menu_formset.is_valid() and hours_formset.is_valid() :
            response = super(EatUpdateView, self).form_valid(form)
            images_formset.instance = self.object
            images_formset.save()
            menu_formset.instance = self.object
            menu_formset.save()
            hours_formset.instance = self.object
            hours_formset.save()
            return response
        else:
            return super(EatUpdateView, self).form_invalid(form)


@method_decorator([login_required, ], name='dispatch')
class EatDeleteView(SuccessMessageMixin, SellerEatMixin, DeleteView, PermissionRequiredMixin):
    template_name = 'kirinyaga/eat_delete.html'
    success_url = reverse_lazy('kirinyaga:my_eats')

    success_message = 'Successfully Deleted'


@login_required
def dashboard(request):
    return render(request, 'kirinyaga/dashboard.html')


class PartnerRegistrationView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'kirinyaga/registration.html'
    form_class = PartnerRegistrationForm
    success_url = reverse_lazy('kirinyaga:dashboard')
    success_message = 'Account Successfully Created.'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'partner'
        return super(PartnerRegistrationView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        result = super(PartnerRegistrationView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password1'],


                            )

        login(self.request, user)
        return result





