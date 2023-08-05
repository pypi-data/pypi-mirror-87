from django.forms import ModelForm
from .models import Activity, Actor


class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['type', 'actor', 'when', 'description']


class ActorForm(ModelForm):
    class Meta:
        model = Actor
        fields = ['name', 'telephone', 'cellphone', 'email']
