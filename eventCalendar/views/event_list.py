from django.views.generic import ListView

from eventCalendar.models import Event


class AllEventsListView(ListView):
    """ All event list views """

    template_name = "events/calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_all_events()


class RunningEventsListView(ListView):
    """ Running events list view """

    template_name = "events/calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_running_events()


class UpcomingEventsListView(ListView):
    """ upcoming events list view """

    template_name = "events/calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_running_events()
