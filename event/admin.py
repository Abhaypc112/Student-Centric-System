from django.contrib import admin
from .models import staff,student,EventDetails
# Register your models here.



class staffAdmin(admin.ModelAdmin):
    pass
admin.site.register(staff, staffAdmin)

class studentAdmin(admin.ModelAdmin):
    pass
admin.site.register(student, studentAdmin)

class EventDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(EventDetails, EventDetailsAdmin)




