from __future__ import unicode_literals
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    is_profile = models.BooleanField(default=False)
    is_finder = models.BooleanField(default=False)


class SubCounty(models.Model):
    name = models.CharField(max_length=50)
    detail = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='date_added')

    class Meta:
        ordering = ('-date_added',)
        verbose_name_plural = 'SubCounties'

    def __str__(self):
        return self.name


class Attraction(models.Model):

    name = models.CharField(max_length=200)
    tag_line = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=250, unique_for_date='date_added')
    date_added = models.DateTimeField(auto_now=True)
    detail = models.TextField()
    tags = TaggableManager(blank=True)
    sub_county = models.ForeignKey(SubCounty, related_name='attractions')
    photo = ProcessedImageField(upload_to='attractions', processors=[ResizeToFill(512, 380)],
                                format='JPEG',
                                options={'quality': 100}, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('kirinyaga:attraction-detail', args=[self.date_added.year,
                                                 self.date_added.strftime('%m'),
                                                 self.date_added.strftime('%d'),
                                                 self.slug])


class Image(models.Model):
    title = models.CharField(max_length=100, blank=True)
    date_added = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(upload_to='images', processors=[ResizeToFill(512, 380)],
                                format='JPEG',
                                options={'quality': 100})
    attraction = models.ForeignKey(Attraction, related_name='images')

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.title


class Highlight(models.Model):
    title = models.CharField(max_length=100, blank=True)
    date_added = models.DateTimeField(auto_now=True)

    attraction = models.ForeignKey(Attraction, related_name='highlights')

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.title


class Vital(models.Model):
    title = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now=True)

    attraction = models.ForeignKey(Attraction, related_name='vitals')

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.title


class Place(models.Model):
    STATUS = (
        ('draft', 'Draft'),
        ('published', 'Published'),


    )
    provider = models.ForeignKey(User, related_name='places')
    sub_county = models.ForeignKey(SubCounty, related_name='places')
    tag_line = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    photo = ProcessedImageField(upload_to='images', processors=[ResizeToFill(512, 380)],
                                format='JPEG',
                                options={'quality': 100})
    phone = PhoneNumberField()
    website = models.URLField(blank=True)
    detail = models.TextField()
    date_added = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=100)
    tags = TaggableManager(blank=True)
    status = models.CharField(max_length=200, choices=STATUS, default='draft')

    def save(self, *args, **kwargs):
        super(Place, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name) + "-" + str(self.id)
            self.save()

    def get_absolute_url(self):
        return reverse('kirinyaga:place-detail', args=[self.date_added.year,
                                                            self.date_added.strftime('%m'),
                                                            self.date_added.strftime('%d'),
                                                            self.slug])


class Facility(models.Model):
    place = models.ForeignKey(Place, related_name='facilities')
    name = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now=True)
    photo = ProcessedImageField(upload_to='images', processors=[ResizeToFill(512, 380)],
                                format='JPEG',
                                options={'quality': 100})

    class Meta:
        ordering = ('-date_added',)
        verbose_name_plural = 'Facilities'


class Activity(models.Model):
    place = models.ForeignKey(Place, related_name='activities')
    name = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now=True)
    photo = ProcessedImageField(upload_to='images', processors=[ResizeToFill(512, 380)],
                                format='JPEG',
                                options={'quality': 100})

    class Meta:
        ordering = ('-date_added',)
        verbose_name_plural = 'Activities'


class PlaceImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    date_added = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(upload_to='place_images', processors=[ResizeToFill(512, 380)],
                                format='JPEG',
                                options={'quality': 100})
    place = models.ForeignKey(Place, related_name='place_images')

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.title


class Interest(models.Model):
    name = models.CharField(max_length=100, blank=True)
    date_added = models.DateTimeField(auto_now=True)

    place = models.ForeignKey(Place, related_name='interest')

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name


class StayType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Stay(models.Model):
    STATUS = (
        ('draft', 'Draft'),
        ('published', 'Published'),

    )
    sub_county = models.ForeignKey(SubCounty, related_name='sub_counties')
    provider = models.ForeignKey(User, related_name='stays')
    tag_line = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, help_text='If you do not have a website leave the field blank ')
    stay_type = models.ForeignKey(StayType, related_name='stays')
    rooms = models.PositiveIntegerField()
    description = models.TextField()
    photo = ProcessedImageField(upload_to='images', processors=[ResizeToFill(512, 380)],
                                format='JPEG',
                                options={'quality': 100})
    location = models.CharField(max_length=200)
    phone = PhoneNumberField(help_text='Use +254 format')
    date_added = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200)
    tags = TaggableManager(blank=True)
    status = models.CharField(max_length=200, choices=STATUS, default='draft')

    def save(self, *args, **kwargs):
        super(Stay, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name) + "-" + str(self.id)
            self.save()

    def get_absolute_url(self):
        return reverse('kirinyaga:stay-detail', args=[self.date_added.year,
                                                       self.date_added.strftime('%m'),
                                                       self.date_added.strftime('%d'),
                                                       self.slug])


class StayImage(models.Model):
    date_added = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(upload_to='stay_images', processors=[ResizeToFill(512, 380)],
                                format='JPEG',
                                options={'quality': 100})
    stay = models.ForeignKey(Stay, related_name='stay_images')

    class Meta:
        ordering = ('-date_added',)


class StayFacility(models.Model):
    stay = models.ForeignKey(Stay, related_name='stay_facilities')
    name = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now=True)
    photo = ProcessedImageField(upload_to='stay_facilities', processors=[ResizeToFill(512, 380)],
                                format='JPEG',
                                options={'quality': 100})

    class Meta:
        ordering = ('-date_added',)
        verbose_name_plural = 'StayFacilities'


class Term(models.Model):
    title = models.CharField(max_length=200, blank=True)
    date_added = models.DateTimeField(auto_now=True)

    stay = models.ForeignKey(Stay, related_name='terms')

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.title


class InterestingPlace(models.Model):
    title = models.CharField(max_length=200, blank=True)
    date_added = models.DateTimeField(auto_now=True)

    stay = models.ForeignKey(Stay, related_name='interesting_places')

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.title


class RoomType(models.Model):
    stay = models.ForeignKey(Stay, related_name='room_types')
    name = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now=True)
    photo = ProcessedImageField(upload_to='rooms', processors=[ResizeToFill(512, 380)],
                                format='JPEG',
                                options={'quality': 100})
    price = models.PositiveIntegerField()

    class Meta:
        ordering = ('-date_added',)
        verbose_name_plural = 'RoomTypes'


class Eat(models.Model):
    STATUS = (
        ('draft', 'Draft'),
        ('published', 'Published'),

    )
    name = models.CharField(max_length=200)
    provider = models.ForeignKey(User, related_name='eats')
    tag_line = models.CharField(max_length=200, blank=True)
    sub_county = models.ForeignKey(SubCounty, related_name='eats')
    phone = PhoneNumberField()
    description = models.TextField()
    tags = TaggableManager(blank=True)
    date_added = models.DateTimeField(auto_now=True)
    photo = ProcessedImageField(upload_to='eats', processors=[ResizeToFill(512, 380)],
                                format='JPEG',
                                options={'quality': 100})
    slug = models.SlugField(max_length=200)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=200, choices=STATUS, default='draft')

    def save(self, *args, **kwargs):
        super(Eat, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name) + "-" + str(self.id)
            self.save()

    def get_absolute_url(self):
        return reverse('kirinyaga:eat-detail', args=[self.date_added.year,
                                                      self.date_added.strftime('%m'),
                                                      self.date_added.strftime('%d'),
                                                      self.slug])


class EatImage(models.Model):
    date_added = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(upload_to='eat_images', processors=[ResizeToFill(512, 380)],
                                format='JPEG',
                                options={'quality': 100})
    eat = models.ForeignKey(Eat, related_name='eat_images')

    class Meta:
        ordering = ('-date_added',)

 
class Menu(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now=True)

    eat = models.ForeignKey(Eat, related_name='menus')

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name


class OpeningHours(models.Model):
    DAYS = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),

    )
    date_added = models.DateTimeField(auto_now=True)
    eat = models.ForeignKey(Eat, related_name='opening_hours')
    day = models.CharField(max_length=200, choices=DAYS)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

