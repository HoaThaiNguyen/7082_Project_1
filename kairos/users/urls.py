from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('login/', views.login_view, name="login"),
]
