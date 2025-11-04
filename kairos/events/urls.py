from django.urls import path
from . import views

urlpatterns = [
    path('', views.events),
    path('events/', views.user_events, name='user_events'),
]
