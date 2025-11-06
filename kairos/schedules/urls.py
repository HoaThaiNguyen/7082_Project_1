from django.urls import path
from . import views

urlpatterns = [
    path('<slug:event_id>/', views.availability_calendar, name='schedule'),
]
