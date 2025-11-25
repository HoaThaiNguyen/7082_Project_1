from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit', views.edit_profile, name='edit'),
    path('login/', views.login_view, name="login"),
]
