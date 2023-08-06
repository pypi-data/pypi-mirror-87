from django.db import models
from datetime import date
from django.db.models.deletion import CASCADE
from dcim.models import Device


class ActivityInstallOptions(models.TextChoices):
    INSTALL = 'IN-RMA', 'Instalação/Retorno de RMA'
    INSTALLMODER = 'IN-MO', 'Instalação/Modernização'
    INSTALLTEMP = 'IN-TP', 'Instalação/Temporária'
    INSTALLPON = 'IN-NP', 'Instalação/Novos pontos'
    INSTALLORG = 'IN-OR', 'Instalação/Organização de rack/instalação'


class Actor(models.Model):

    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    cellphone = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Activity(models.Model):

    actor = models.ManyToManyField(Actor)
    type = models.CharField(
        max_length=6,
        choices=ActivityInstallOptions.choices,
        default=ActivityInstallOptions.INSTALL,
    )

    when = models.DateField(default=date.today)
    description = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.description


class OldDevice(models.Model):
    activity = models.OneToOneField(Activity, on_delete=CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    rack = models.CharField(max_length=100, null=True, blank=True)
    site = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=30, null=True, blank=True)
    ipv4 = models.CharField(max_length=40, null=True, blank=True)
    masc_ipv4 = models.CharField(max_length=40, null=True, blank=True)
    ipv6 = models.CharField(max_length=70, null=True, blank=True)
    masc_ipv6 = models.CharField(max_length=70, null=True, blank=True)
    mac = models.CharField(max_length=12, null=True, blank=True)
    tombo = models.CharField(max_length=30, null=True, blank=True)
    serial = models.CharField(max_length=30, null=True, blank=True)
