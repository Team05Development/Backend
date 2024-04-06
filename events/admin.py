from django.contrib import admin

from .models_event import Event, Program, Favorites
from .models_auxiliary import Direction, Format, EventStatus, ApplicationStatus
from .models_application import Application

admin.site.register(Event)
admin.site.register(Program)
admin.site.register(Favorites)
admin.site.register(Direction)
admin.site.register(Format)
admin.site.register(EventStatus)
admin.site.register(ApplicationStatus)
admin.site.register(Application)