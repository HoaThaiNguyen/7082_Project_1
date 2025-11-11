from django.urls import path
from . import views

urlpatterns = [
    # path('', views.events),
    path('', views.events, name='list'),
]
