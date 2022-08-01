from django.contrib import admin
from .models import Application, Blog, Latest, Testimonial
import csv
import datetime
from django.http import HttpResponse


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Dispostion'] = 'attachment; \ filename= {}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to csv'


class TestimonialAdmin(admin.ModelAdmin):
    list_filter = ('person', )
    list_display = ('person', )
    search_fields = ('created', 'title')
    date_hierarchy = 'created'
    ordering = ('created',)
admin.site.register(Testimonial, TestimonialAdmin)


class LatestAdmin(admin.ModelAdmin):
    list_filter = ('title', )
    list_display = ('title', )
    search_fields = ('created', 'person')
    date_hierarchy = 'created'
    ordering = ('created',)
admin.site.register(Latest, LatestAdmin)

