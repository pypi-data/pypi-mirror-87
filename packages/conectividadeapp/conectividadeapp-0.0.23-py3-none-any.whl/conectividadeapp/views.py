from django.shortcuts import render, redirect, get_object_or_404
from .models import Activity, Actor
from .forms import ActorForm
from django.http import HttpResponse
import datetime
from django.views.generic import View
from dcim.models import Device, DeviceRole
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# from django.db.models import Q


class ListConectividadeView(LoginRequiredMixin, View):
    """
    List all reg in the database.
    """

    rg = Activity.objects.all()
    dv = Device.objects.all()
    dr = DeviceRole.objects.all()

    def get(self, request):

        rg = Activity.objects.all()
        dv = Device.objects.all()
        dr = DeviceRole.objects.all()

        return render(request, 'conectividadeapp/listagem.html', {
            'registro': rg,
            'device': dv,
            'devicerole': dr,

        })

    def post(self, request):

        rg = Activity.objects.all()
        dr = DeviceRole.objects.all()
        dv = Device.objects.all()

        data = {}
        data['papel'] = request.POST['role']
        data['deviceid'] = request.POST['deviceid']
        data['devicerole'] = dr
        data['registro'] = rg
        device_ob = Device.objects.get(id=data['deviceid'])

        # fazer tratamento
        data['device_obj'] = device_ob

        return render(request, 'conectividadeapp/listagem.html', data)


'''
Activity Filter Views
'''


# All activities
class ActivityAllListView(View):

    def get(self, request):
        activities = Activity.objects.all().order_by('-when')

        context = {
            'activities': activities
        }

        return render(request, 'conectividadeapp/activity_list.html', context)


# Activities filtered by year
class ActivityYearListView(View):

    def get(self, request, year):
        activities = Activity.objects.all().filter(when__year=year).order_by('-when')

        context = {
            'activities': activities
        }

        return render(request, 'conectividadeapp/activity_list.html', context)


# Activities filtered by year and month
class ActivityMonthListView(View):

    def get(self, request, year, month):
        activities = Activity.objects.all().filter(when__year=year, when__month=month).order_by('-when')

        context = {
            'activities': activities
        }

        return render(request, 'conectividadeapp/activity_list.html', context)


# Activities filtered by year, month and day
class ActivityDayListView(View):

    def get(self, request, year, month, day):
        activities = Activity.objects.all().filter(when__year=year, when__month=month, when__day=day).order_by('-when')

        context = {
            'activities': activities
        }

        return render(request, 'conectividadeapp/activity_list.html', context)


class CreateActor(CreateView):
    model = Actor
    form_class = ActorForm
    template_name = 'conectividadeapp/addactor.html'
    queryset = Actor.objects.all()
    success_url = reverse_lazy('list')
