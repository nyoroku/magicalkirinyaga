from __future__ import unicode_literals
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

from django.db import models


class Category(models.Model):

    title = models.CharField(max_length=50)
    detail = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_added',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Trip(models.Model):
    AVAILABILITY = (
        ('yes', 'YES'),
        ('no', 'NO'))
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique_for_date='date_added', default='trips')
    date_added = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    detail = models.TextField()
    start = models.DateField(blank=True)
    End = models.DateField(blank=True)
    summary = models.TextField()
    category = models.ForeignKey(Category)
    included = models.TextField()
    excluded = models.TextField()
    availability = models.CharField(max_length=50, choices=AVAILABILITY, default='no')
    photo = ProcessedImageField(upload_to='trips', processors=[ResizeToFill(1778, 1000)],
                                format='JPEG',
                                options={'quality': 100}, blank=True)
    tags = TaggableManager()


    class Meta:
        ordering = ('-date_added',)
        verbose_name_plural = 'Trips'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tour:trip-detail', args=[self.date_added.year,
                                                   self.date_added.strftime('%m'),
                                                   self.date_added.strftime('%d'),
                                                   self.slug])


class Image(models.Model):
    title = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(upload_to='images', processors=[ResizeToFill(1024, 767)],
                                format='JPEG',
                                options={'quality': 100})
    trip = models.ForeignKey(Trip, related_name='images')

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.title





