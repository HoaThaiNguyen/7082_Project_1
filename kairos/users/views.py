from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

# Create your views here.

# @login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("events:list")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form":form})