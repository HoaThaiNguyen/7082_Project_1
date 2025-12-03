from django.urls import path
from . import views

urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('create/', views.group_create, name='group_create'),
    path('<int:group_id>/', views.group_detail, name='group_detail'),
]
