from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # path('', views.events),
    path('', views.events, name="list"),
    path('events/', views.user_events, name='user_events'),
]
