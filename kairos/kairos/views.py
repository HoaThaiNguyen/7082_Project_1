from django.shortcuts import render


def homepage(request):
    return render(request, 'home.html')


# def login_page(request):
#     return render(request, 'login.html')


# def signup_page(request):
#     return render(request, 'signup.html')


def events_page(request):
    return render(request, "events/events.html")
