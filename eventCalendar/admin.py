from django.contrib import admin
from eventCalendar.models import event, event_abstract

@admin.register(event.Event)
class EventAdmin(admin.ModelAdmin):
    model = event.Event
    list_display = [
        "id",
        "title",
        "is_active",
        "is_deleted",
        "created_at",
        "updated_at",
    ]
    list_filter = ["is_active", "is_deleted"]
    search_fields = ["title"]

