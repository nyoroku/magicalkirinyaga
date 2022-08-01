from django.contrib import admin
from .models import SubCounty, Attraction, Image,Highlight,Vital, PlaceImage, Facility, Activity, Eat,Menu,EatImage, OpeningHours, Place,StayType, Interest,Stay,Term, StayFacility,StayImage,InterestingPlace,RoomType






class SubCountyAdmin(admin.ModelAdmin):
    list_filter = ('name', 'date_added')
    list_display = ('name', 'detail')
    search_fields = ('date_added', 'name')
    date_hierarchy = 'date_added'
    ordering = ('date_added',)
admin.site.register(SubCounty, SubCountyAdmin)


class ImageAdminInline(admin.TabularInline):
    model = Image


class HighlightAdminInline(admin.TabularInline):
    model = Highlight


class VitalAdminInline(admin.TabularInline):
    model = Vital


class AttractionAdmin(admin.ModelAdmin):
    list_filter = ('name', 'date_added')
    list_display = ('name', 'detail')
    search_fields = ('date_added', 'name')
    date_hierarchy = 'date_added'
    ordering = ('date_added',)
    inlines = (ImageAdminInline, HighlightAdminInline, VitalAdminInline)
admin.site.register(Attraction, AttractionAdmin)


class PlaceImageAdminInline(admin.TabularInline):
    model = PlaceImage


class FacilityAdminInline(admin.TabularInline):
    model = Facility


class ActivityAdminInline(admin.TabularInline):
    model = Activity


class InterestAdminInline(admin.TabularInline):
    model = Interest


class PlaceAdmin(admin.ModelAdmin):
    list_filter = ('name', 'date_added')
    list_display = ('name', 'date_added')
    search_fields = ('date_added', 'name')
    date_hierarchy = 'date_added'
    ordering = ('date_added',)
    inlines = (PlaceImageAdminInline, FacilityAdminInline, ActivityAdminInline, InterestAdminInline)
admin.site.register(Place, PlaceAdmin)


class StayTypeAdmin(admin.ModelAdmin):
    list_filter = ('name',)

admin.site.register(StayType, StayTypeAdmin)


class StayImageAdminInline(admin.TabularInline):
    model = StayImage


class RoomTypeAdminInline(admin.TabularInline):
    model = RoomType


class StayFacilityAdminInline(admin.TabularInline):
    model = StayFacility


class StayNearbyAdminInline(admin.TabularInline):
    model = InterestingPlace


class TermsAdminInline(admin.TabularInline):
    model = Term


class StayAdmin(admin.ModelAdmin):
    list_filter = ('name', 'date_added')
    list_display = ('name', 'date_added')
    search_fields = ('date_added', 'name')
    date_hierarchy = 'date_added'
    ordering = ('date_added',)
    inlines = (StayImageAdminInline, RoomTypeAdminInline, StayFacilityAdminInline, StayNearbyAdminInline, TermsAdminInline)
admin.site.register(Stay, StayAdmin)


class EatImageAdminInline(admin.TabularInline):
    model = EatImage


class MenuAdminInline(admin.TabularInline):
    model = Menu


class OpeningHourAdminInline(admin.TabularInline):
    model = OpeningHours


class EatAdmin(admin.ModelAdmin):
    list_filter = ('name', 'date_added')
    list_display = ('name', 'date_added')
    search_fields = ('date_added', 'name')
    date_hierarchy = 'date_added'
    ordering = ('date_added',)
    inlines = (EatImageAdminInline, MenuAdminInline, OpeningHourAdminInline)

admin.site.register(Eat, EatAdmin)
