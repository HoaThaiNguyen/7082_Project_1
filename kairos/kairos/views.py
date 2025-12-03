from django.shortcuts import render


def homepage(request):
    return render(request, 'home.html')


def events_page(request):
    return render(request, "events/events.html")
