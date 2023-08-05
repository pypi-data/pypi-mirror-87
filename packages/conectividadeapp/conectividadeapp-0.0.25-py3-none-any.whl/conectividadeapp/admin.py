
from django.contrib import admin
from .models import Activity
from .models import Actor
from .models import OldDevice


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'type']


@admin.register(OldDevice)
class OldDevice(admin.ModelAdmin):
    list_display = ['id']


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
   list_display = ('id', 'name')
