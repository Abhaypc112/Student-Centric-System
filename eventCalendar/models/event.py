from datetime import datetime
from django.db import models
from django.urls import reverse

from eventCalendar.models import EventAbstract



class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self): 

        events = Event.objects.all()             
        return events

    def get_running_events(self): 
        running_events = Event.objects.filter(
            
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")
        return running_events
    
    def get_upcoming_events(self):
        upcoming_events = Event.objects.filter(
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),).order_by("start_time")
        return upcoming_events

class Event(EventAbstract):
    """ Event model """

   
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    objects = EventManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("eventCalendar:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("eventCalendar:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
