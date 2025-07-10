from django.contrib import admin

from .models import Flat, Complaint, Owner


class FlatsInstanceInline(admin.TabularInline):
    model = Flat.owners.through
    raw_id_fields = ['owner']


class FlatAdmin(admin.ModelAdmin):
    search_fields = ('town', 'address')
    readonly_fields = ['created_at']
    list_display = [
        'address',
        'price',
        'new_building',
        'construction_year',
        'town'
    ]
    list_editable = ['new_building']
    list_filter = ['new_building', 'created_at', 'rooms_number', 'active']
    raw_id_fields = ['liked_by']
    inlines = [FlatsInstanceInline]


class ComplaintAdmin(admin.ModelAdmin):
    raw_id_fields = ['author', 'flat']


class OwnerAdmin(admin.ModelAdmin):
    raw_id_fields = ['flats']


admin.site.register(Flat, FlatAdmin)
admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Owner, OwnerAdmin)
