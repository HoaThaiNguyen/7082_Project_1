from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path('', views.get_notifications, name="get_notifications"),
    path('mark-read/<int:notification_id>/', views.mark_notification_read, name="mark_notification_read"),
    path('has-unread-notifications', views.has_unread_notifications, name='has_unread_notifications'),

    path('clear', views.clear_notifications, name="clear")
]
