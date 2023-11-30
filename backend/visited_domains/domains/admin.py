from django.contrib import admin
from .models import Domain
from rangefilter.filters import DateTimeRangeFilter


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'created'
    )
    search_fields = (
        'name',
    )
    readonly_fields = (
        'created',
    )
    list_filter = (
        ('created', DateTimeRangeFilter),
        'name'
    )
