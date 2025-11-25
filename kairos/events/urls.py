from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # path('', views.events),
    path('', views.events, name='list'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/yes/', views.rsvp_yes, name='rsvp_yes'),
    path('<int:event_id>/no/', views.rsvp_no, name='rsvp_no'),
    path('<slug:event_id>/', views.availability_calendar, name='schedule'),
]
