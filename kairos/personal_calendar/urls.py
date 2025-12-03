from django.urls import path
from . import views

app_name = "personal_calendar"

urlpatterns = [
    path('', views.personal_calendar_view, name='personal_calendar'),
    path('edit/<int:pk>/', views.edit_recurring_time, name='edit_recurring_time'),
    path('delete/<int:pk>/', views.delete_recurring_time, name='delete_recurring_time'),
]