from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_harvester_activity, name='add_activity'),
    path('success/', views.activity_success, name='activity_success'),
    path('download/', views.download_activities_csv, name='download_activities'),  # new
]