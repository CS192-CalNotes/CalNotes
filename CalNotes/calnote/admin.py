from django.contrib import admin
from .models import Task, Event, Note

admin.site.register(Task)
admin.site.register(Event)
admin.site.register(Note)