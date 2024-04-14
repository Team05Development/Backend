from django.contrib import admin

from .models_event import Event, Program
from .models_favorites import Favorites
from .models_auxiliary import Direction, Format, EventStatus, ApplicationStatus
from .models_application import Application


class ProgramInline(admin.TabularInline):
    model = Program
    extra = 1
    # min_num = 1

    # def get_formset(self, request, obj=None, **kwargs):
    #     formset = super().get_formset(request, obj=None, **kwargs)
    #     formset.validate_min = True
    #     return formset

class EventAdmin(admin.ModelAdmin):
    inlines = (
        ProgramInline,        
    )

admin.site.register(Event, EventAdmin)
admin.site.register(Program)
admin.site.register(Favorites)
admin.site.register(Direction)
admin.site.register(Format)
admin.site.register(EventStatus)
admin.site.register(ApplicationStatus)
admin.site.register(Application)