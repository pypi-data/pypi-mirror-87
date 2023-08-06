from django import forms
from django.forms import ModelForm
from .models import Activity, Actor
from utilities.forms import BootstrapMixin

BLANK_CHOICE = (("", "---------"),)


class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['type', 'actor', 'when', 'description']


class ActorForm(ModelForm):
    class Meta:
        model = Actor
        fields = ['name', 'telephone', 'cellphone', 'email']


class ActorFilterForm(BootstrapMixin, forms.ModelForm):
    q = forms.CharField(
        required=False,
        label="Search",
    )

    class Meta:
        model = Actor
        fields = [
            'q',
        ]
