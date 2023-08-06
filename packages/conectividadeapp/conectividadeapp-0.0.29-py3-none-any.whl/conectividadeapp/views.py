import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db.models import Q

from dcim.models import Device, DeviceRole

from .forms import ActivityForm, ActorForm
from .models import Activity, Actor


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
        data['deviceid'] = request.POST['deviceid']
        data['devicerole'] = dr
        data['registro'] = rg
        data['device'] = dv
        data['form'] = ActivityForm()

        if data['deviceid']:
            device_ob = Device.objects.get(id=data['deviceid'])
            data['device_obj'] = device_ob
            # fazer tratamento
        else:
            data['device_obj'] = []

        return render(request, 'conectividadeapp/listagem.html', data)


class CreateactivityView(LoginRequiredMixin, View):
    def get(self, request):
        pass

    def post(self, request):
        data = {}
        data['activities'] = Activity.objects.all()

        form = ActivityForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'conectividadeapp/activity_list.html', data)


# Activity List Views
class ActivityListView(LoginRequiredMixin, View):

    def get(self, request):

        # Request setup for filter
        r = request.GET

        if r.get('year_month') is not None:
            year_month = datetime.datetime.strptime(r.get('year_month'), '%Y-%m')
            year = year_month.year
            month = year_month.month

            activity_list = Activity.objects.filter(
                when__year=year,
                when__month=month,
            ).order_by('-when')
        else:
            activity_list = Activity.objects.all().order_by('-when')

        # Search filter conditions
        # if year is not None and month is not None and day is not None:
        #     activity_list = Activity.objects.all().filter(
        #         when__year = year,
        #         when__month = month,
        #         when__day = day
        #     ).order_by('-when')
        # elif year is not None and month is not None and day is None:
        #     activity_list = Activity.objects.all().filter(
        #         when__year = year,
        #         when__month = month
        #     ).order_by('-when')
        # elif year is not None and month is None and day is None:
        #     activity_list = Activity.objects.all().filter(
        #         when__year = year
        #     ).order_by('-when')
        # elif year is None and month is None and day is None:
        #     activity_list = Activity.objects.all().order_by('-when')
        # else:
        #     return redirect('plugins:conectividadeapp:activity_list')

        # Quantity of activities after the filter
        quantity = len(activity_list)

        # Current year
        current_year = datetime.date.today().year
        current_month = datetime.date.today().month

        # Template to be rendered
        template_name = 'conectividadeapp/activity_list.html'

        # Context dictionary for rendering
        context = {
            'activity_list': activity_list,
            'quantity': quantity,
            'current_year': current_year,
            'current_month': current_month,
        }

        return render(request, template_name, context)


class CreateActor(LoginRequiredMixin, CreateView):
    model = Actor
    form_class = ActorForm
    template_name = 'conectividadeapp/addactor.html'
    queryset = Actor.objects.all()
    success_url = reverse_lazy('list')


class ListDeviceView(LoginRequiredMixin, ListView):
    model = Device
    template_name = 'conectividadeapp/searchdevice.html'


class SearchDeviceView(LoginRequiredMixin, ListView):
    model = Device
    template_name = 'conectividadeapp/searchdeviceresult.html'

    def get_queryset(self):

        query = self.request.GET.get('q')
        object_list = Device.objects.filter(
            Q(asset_tag__icontains=query)
        )
        return object_list
