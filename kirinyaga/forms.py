from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .models import Place, PlaceImage, User, Facility, Activity, Interest, Stay, StayImage, StayFacility, RoomType, InterestingPlace, Term, Eat, EatImage, OpeningHours, Menu
from django.db import transaction
from phonenumber_field.formfields import PhoneNumberField
from dal import autocomplete


class PlaceForm(forms.ModelForm):

    class Meta:
        model = Place
        fields = ('name',  'tag_line', 'sub_county', 'location', 'phone', 'website', 'detail', 'photo'

                  )


class StayForm(forms.ModelForm):

    class Meta:
        model = Stay
        fields = ('name', 'tag_line', 'stay_type', 'rooms', 'sub_county', 'location', 'phone', 'website', 'description', 'photo'

                  )

PlaceImageFormSet = inlineformset_factory(Place, PlaceImage, fields=['title', 'image'], extra=10, can_delete=True)
PlaceFacilityFormSet = inlineformset_factory(Place, Facility, fields=['name', 'photo'], extra=10, can_delete=True)
PlaceActivityFormSet = inlineformset_factory(Place, Activity, fields=['name', 'photo'], extra=10, can_delete=True)
PlaceInterestFormSet = inlineformset_factory(Place, Interest, fields=['name', ], extra=10, can_delete=True)
StayImageFormSet = inlineformset_factory(Stay, StayImage, fields=['image'], extra=10, can_delete=True)
StayFacilityFormSet = inlineformset_factory(Stay, StayFacility, fields=['name', 'photo'], extra=10, can_delete=True)
StayRoomFormSet = inlineformset_factory(Stay, RoomType, fields=['name', 'price', 'photo'], extra=10, can_delete=True)
StayInterestFormSet = inlineformset_factory(Stay, InterestingPlace, fields=['title', ], extra=10, can_delete=True)
StayTermFormSet = inlineformset_factory(Stay, Term, fields=['title', ], extra=10, can_delete=True)
EatImageFormSet = inlineformset_factory(Eat, EatImage, fields=['image'], extra=10, can_delete=True)
EatMenuFormset = inlineformset_factory(Eat, Menu, fields=['name', 'price', 'description'], extra=10, can_delete=True)
OpeningHoursFormset = inlineformset_factory(Eat, OpeningHours, fields=['day', 'opening_time', 'closing_time'], extra=10, can_delete=True)

class EatForm(forms.ModelForm):

    class Meta:
        model = Eat
        fields = ('name', 'tag_line', 'sub_county', 'location', 'phone', 'website', 'description', 'photo')


class PartnerRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=80, help_text='Required. Use avalid email', label='Email')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'password2', 'password1', 'username')

    def save(self, commit=True):
        user = super(PartnerRegistrationForm, self).save(commit=False)
        user.is_finder = True
        if commit:
            user.save()
        return user





