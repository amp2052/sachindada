from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "phone",   # ✅ FIXED
        "grievance_type",
        "created_at",
        "is_read"
    )

    list_filter = (
        "grievance_type",
        "is_read",
        "created_at"
    )

    search_fields = (
        "name",
        "email",
        "phone",   # ✅ FIXED
        "message"
    )

    ordering = ("-created_at",)

    list_editable = ("is_read",)

    readonly_fields = ("created_at",)

    fieldsets = (
        ("User Information", {
            "fields": ("name", "email", "phone")  # ✅ FIXED
        }),

        ("Message Details", {
            "fields": ("subject", "grievance_type", "message")
        }),

        ("Status", {
            "fields": ("is_read", "created_at")
        }),
    )
    
from django.contrib import admin
from .models import Volunteer

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    search_fields = ['name', 'email', 'phone']
    list_filter = ['created_at']
from django.contrib import admin
from .models import Gallery, News

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    
    
    
    
    
    
    
    
    
    
    
    from django.contrib import admin
from .models import IssueReport

@admin.register(IssueReport)
class IssueReportAdmin(admin.ModelAdmin):

    list_display = ('name', 'village', 'main_issue', 'severity', 'created_at')
    list_filter = ('main_issue', 'severity', 'priority', 'scheme')
    search_fields = ('name', 'village', 'phone')




    ordering = ('-created_at',)