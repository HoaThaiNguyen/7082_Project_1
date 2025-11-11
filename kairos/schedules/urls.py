from django.urls import path
from . import views

urlpatterns = [
    path('', views.busy_times_view, name='busy_times'),
]
