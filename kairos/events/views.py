from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, BusyTime, Participation
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User


# Create your views here.


@login_required(login_url='login')
def events(request):
    search = request.GET.get("search")
    sort = request.GET.get("sort")
    events = Event.objects.all()
    
    if search != None:
        events = events.filter(title__icontains=search)

    if sort != None:
        if sort == "most-recent":
            events = events.order_by("date")
        elif sort == "least-recent":
            events = events.order_by("-date")
        elif sort == "alphabetical-increasing":
            events = sorted(events, key=lambda x: x.title)
        elif sort == "alphabetical-decreasing":
            events = sorted(events, key=lambda x: x.title, reverse=True)

    #print("DEBUG - Events fetched:", events)
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


@login_required(login_url='/login/')
def rsvp_yes(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Participation.objects.update_or_create(
        user=request.user,
        event=event,
        defaults={'status': 'yes'}
    )
    return redirect('events:event_detail', event_id=event.id)


@login_required(login_url='/login/')
def rsvp_no(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Participation.objects.update_or_create(
        user=request.user,
        event=event,
        defaults={'status': 'no'}
    )
    return redirect('events:event_detail', event_id=event.id)


@login_required(login_url='/login/')
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    yes = Participation.objects.filter(event=event, status='yes')
    no = Participation.objects.filter(event=event, status='no')
    responded_users = Participation.objects.filter(
        event=event).values_list('user_id', flat=True)
    not_responded = User.objects.exclude(id__in=responded_users)

    context = {
        'event': event,
        'yes': yes,
        'no': no,
        'not_responded': not_responded
    }
    return render(request, 'events/event_detail.html', context)
