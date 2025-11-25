from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, BusyTime, Participation, AvailabilityBlock
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
import json
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.http import HttpResponseForbidden


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

def availability_calendar(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    context = {
        "event": event,
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


@login_required
def load_availability(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)

    blocks = AvailabilityBlock.objects.filter(
        user=request.user,
        event=event
    )

    response = [
        {
            "start": block.start.isoformat(),
            "end": block.end.isoformat(),
        }
        for block in blocks
    ]

    return JsonResponse({"blocks": response})


@login_required
def save_availability(request, event_slug):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    print("Request body:", request.body)
    event = get_object_or_404(Event, slug=event_slug)
    data = json.loads(request.body)

    # Delete previous blocks for this user/event
    AvailabilityBlock.objects.filter(
        user=request.user,
        event=event
    ).delete()

    # Save new blocks
    for block in data.get("blocks", []):
        start = parse_datetime(block["start"])
        end = parse_datetime(block["end"])
        AvailabilityBlock.objects.create(
            user=request.user,
            event=event,
            start=start,
            end=end
        )

    return JsonResponse({"success": True})


@login_required
def availability_report(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)

    # Allow ONLY event owner
    if request.user != event.owner:
        return HttpResponseForbidden("You are not allowed to view this page.")

    # Load ALL availability for this event
    blocks = (
        AvailabilityBlock.objects
        .filter(event=event)
        .select_related("user")
        .order_by("user__username", "start")
    )

    context = {
        "event": event,
        "blocks": blocks,
    }

    return render(request, "events/availability_report.html", context)
