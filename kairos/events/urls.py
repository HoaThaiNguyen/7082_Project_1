from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # path('', views.events),
    path('', views.events, name='list'),
    path('<slug:event_id>/', views.availability_calendar, name='schedule'),
]
