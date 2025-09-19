from django.contrib import admin
from .models import Contact

# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin configuration for Contact model
    """
    list_display = ('fullname', 'email', 'phone_number', 'country', 'is_active', 'created_at')
    list_filter = ('is_active', 'country', 'created_at')
    search_fields = ('fullname', 'email', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('fullname',)
        }),
        ('Contact Information', {
            'fields': ('email', 'phone_number')
        }),
        ('Address Information', {
            'fields': ('address', 'country'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ('-created_at',)
    list_per_page = 25
