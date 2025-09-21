from django.contrib import admin
from .models import List, Category, Task


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "is_default", "created_at")
    list_filter = ("is_default",)
    search_fields = ("name", "owner__username")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "owner")
    search_fields = ("name", "owner__username")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "owner",
        "list",
        "status",
        "priority",
        "due_date",
        "completed_at",
        "created_at",
    )
    list_filter = ("status", "priority", "list", "categories")
    search_fields = ("title", "owner__username", "description")
    autocomplete_fields = ("list", "categories")
    date_hierarchy = "created_at"

