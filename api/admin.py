from django.contrib import admin
from .models import *


@admin.register(Sponsors)
class SponsorsAdmin(admin.ModelAdmin):
    list_display = ("id", "fish", "phone", "summa", "organization", "type", "status", "payment")
    list_display_links = ("id", "fish")
    list_filter = ("type", "status", "payment")
    date_hierarchy = ("created_at")
    search_fields = ("id", "fish", "phone", "summa", "organization")


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ("id", "fish", "phone", "contract", "otm", "type")
    list_display_links = ("id", "fish")
    list_filter = ("type",)
    date_hierarchy = ("created_at")
    search_fields = ("id", "fish", "phone", "contract", "otm")


admin.site.register(OTMs)