import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import ProfileForm

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

# Create your views here.

# @login_required
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
def profile_view(request):
    return render(request, 'users/profile.html', {'user':request.user})

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def profile_view(request):
#     user = request.user  # automatically identified by the JWT token
#     data = {
#         "username": user.username,
#         "email": user.email,
#         "first_name": user.first_name,
#         "last_name": user.last_name,
#     }
#     return Response(data)

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("events:list")  
    else:
        form = AuthenticationForm()

    return render(request, "users/login.html", {"form":form})


@login_required
def edit_profile(request):
    profile = request.user.profile
    old_pic_path = profile.profile_picture.path if profile.profile_picture else None  # store old file reference
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            new_pic_uploaded = 'profile_picture' in request.FILES
            form.save()

            # delete the old pic when uploaded a new pic
            if new_pic_uploaded and old_pic_path and os.path.exists(old_pic_path): # if a new image is uploaded AND user already had an image
                os.remove(old_pic_path)

            return redirect("users:profile") 
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/edit_profile.html', {'form': form})
