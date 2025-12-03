from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.events, name='list'),

    path('create/', views.create_event, name='create'),

    # integer ID routes FIRST
    path('<slug:event_id>/', views.event_detail, name='event_detail'),
    path('<slug:event_id>/yes/', views.rsvp_yes, name='rsvp_yes'),
    path('<slug:event_id>/no/', views.rsvp_no, name='rsvp_no'),
    path('<slug:event_id>/availability', views.availability_calendar, name='schedule'),
    # slug routes AFTER so they don't steal integers
    path('<slug:event_id>/availability/load/',
         views.load_availability, name='load_availability'),
    path('<slug:event_id>/availability/save/',
         views.save_availability, name='save_availability'),

]
