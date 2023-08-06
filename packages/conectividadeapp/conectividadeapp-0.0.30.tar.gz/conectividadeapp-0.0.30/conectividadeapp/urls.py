from django.urls import path
from . import views

urlpatterns = [

    path('listagem/', views.ListConectividadeView.as_view(), name='list'),

    # Activity URLs
    path('activity/', views.ActivityListView.as_view(), name='activity_list'),

    path('addactivity/', views.CreateactivityView.as_view(), name='addactivity'),

    path('addactor/', views.CreateActor.as_view(), name='addactor'),

    path('actor_list/', views.ActorListView.as_view(), name='actor_list'),

    path('searchdevice/', views.ListDeviceView.as_view(), name='searchdevice'),

    path('searchdeviceresult/', views.SearchDeviceView.as_view(), name='searchdeviceresult'),
]
