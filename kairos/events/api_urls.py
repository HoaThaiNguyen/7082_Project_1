from django.urls import path
from . import api_views

urlpatterns = [
    path('auth/signup/', api_views.api_signup, name='api_signup'),
    path('events/', api_views.user_events, name='api_user_events'),
]
