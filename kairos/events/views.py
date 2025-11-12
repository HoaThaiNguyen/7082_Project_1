from django.shortcuts import render
from .models import Event, BusyTime
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def events(request):
    events = Event.objects.all().order_by('-date')
    print("DEBUG - Events fetched:", events)
    return render(request, 'events/events.html', {'events': events})


# def user_events(request):
#     user = request.user
#     events = user.event_set.all().values('id', 'name', 'date')
#     return Response({'events': list(events)})

# @login_required
def availability_calendar(request, event_id):
    context = {
        "event_id": event_id,
        "today": timezone.now().date(),
    }
    return render(request, "events/schedule.html", context)

