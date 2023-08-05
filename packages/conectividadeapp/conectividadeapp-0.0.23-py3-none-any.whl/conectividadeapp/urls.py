from django.urls import path, re_path
from . import views

urlpatterns = [

    path('listagem/', views.ListConectividadeView.as_view(), name='list'),
    # path('addactivity/<int:pk>/',views.Createactivity.as_view(), name= 'addactivity'),
    # path('addactivity/', views.Createactivity.as_view(), name='device_activity'),
    # path('list', listagem, name='url_listagem'),


    # Activity Filter URLs
    path('activity/', views.ActivityAllListView.as_view(), name='activity_list_all'),
    re_path(r'^activity/(?P<year>[0-9]{4})/$', views.ActivityYearListView.as_view(), name='activity_list_year'),
    re_path(r'^activity/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.ActivityMonthListView.as_view(), name='activity_list_month'),
    re_path(r'^activity/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.ActivityDayListView.as_view(), name='activity_list_day'),
    path('addactor/', views.CreateActor.as_view(), name='addactor'),
]
