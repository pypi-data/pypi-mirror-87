from django.urls import path, re_path
from . import views

""" urlpatterns = [

    path('listagem/', views.ListConectividadeView.as_view(), name='list'),

    # Activity Filter URLs
    path('activity/', views.ActivityAllListView.as_view(), name='activity_list_all'),
    re_path(r'^activity/(?P<year>[0-9]{4})/$', views.ActivityYearListView.as_view(), name='activity_list_year'),
    re_path(r'^activity/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.ActivityMonthListView.as_view(), name='activity_list_month'),
    re_path(r'^activity/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.ActivityDayListView.as_view(), name='activity_list_day'),
    path('addactivity/', views.CreateactivityView.as_view(), name='addactivity'),

    path('addactor/', views.CreateActor.as_view(), name='addactor'),
] """


urlpatterns = [

    path('listagem/', views.ListConectividadeView.as_view(), name='list'),

    # Activity URLs
    path('activity/', views.ActivityListView.as_view(), name='activity_list'),

    path('addactivity/', views.CreateactivityView.as_view(), name='addactivity'),

    path('addactor/', views.CreateActor.as_view(), name='addactor'),

    path('searchdevice/', views.ListDeviceView.as_view(), name='searchdevice'),

    path('searchdeviceresult/', views.SearchDeviceView.as_view(), name='searchdeviceresult'),
]
