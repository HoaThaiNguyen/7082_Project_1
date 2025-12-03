from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, BusyTime, Participation, AvailabilityBlock
from notifications.models import Notification
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
import json
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
import uuid

# Create your views here.


@login_required(login_url='login')
def events(request):
    search = request.GET.get("search")
    sort = request.GET.get("sort")

    events = Event.objects.all()

    print("views.py event ids: ", events.values_list("event_id", flat=True))
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

    return render(request, 'events/events.html', {'events': events})


def availability_calendar(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)
    print("inside availability_calendar view")
    context = {
        "event": event,
        "today": timezone.now().date(),
    }
    return render(request, 'events/schedule.html', context)


@login_required(login_url='/login/')
def rsvp_yes(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)
    Participation.objects.update_or_create(
        user=request.user,
        event=event,
        defaults={'status': 'yes'}
    )

    # Notify the event creator that someone has updated their status
    if request.user != event.creator:
        Notification.objects.create(
            from_user=request.user,
            to_user=event.creator,
            title="Update for " + event.title,
            description=request.user.username + " responded 'yes' for " + event.title,
            url=event_id
        )
    
    return redirect('events:event_detail', event_id=event.event_id)


@login_required(login_url='/login/')
def rsvp_no(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)
    Participation.objects.update_or_create(
        user=request.user,
        event=event,
        defaults={'status': 'no'}
    )

    # Notify the event creator that someone has updated their status
    if request.user != event.creator:
        Notification.objects.create(
            from_user=request.user,
            to_user=event.creator,
            title="Update for " + event.title,
            description=request.user.username + " responded 'no' for " + event.title,
            url=event_id
        )

    return redirect('events:event_detail', event_id=event.event_id)


@login_required(login_url='/login/')
def event_detail(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)

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
def create_event(request):
    if request.method == "POST":
        event_id = request.POST.get("event_id")
        title = request.POST.get("title")
        description = request.POST.get("description")

        start_raw = request.POST.get("start_time")
        end_raw = request.POST.get("end_time")

        # Convert from "2025-01-12T18:30"
        start_dt = datetime.fromisoformat(start_raw)
        end_dt = datetime.fromisoformat(end_raw)

        event = Event.objects.create(
            title=title,
            body=description,
            event_id=event_id,

            start_date=start_dt.date(),
            start_time=start_dt.time(),
            end_date=end_dt.date(),
            end_time=end_dt.time(),
            creator=request.user,
        )

        return redirect("events:event_detail", event_id=event.event_id)
    

@login_required
def delete_event(request, event_id):
    if request.method == "POST":
        event_to_delete = get_object_or_404(Event, event_id=event_id)

        # ensure only the creator of the event is deleting it
        if event_to_delete.creator == request.user:
            # inform all the participants (besides the creator) with a notification
            responded_user_ids = Participation.objects.filter(
            event=event_to_delete).values_list('user_id', flat=True)
            responded_users = User.objects.filter(id__in=responded_user_ids)
            for user in responded_users:
                if user != event_to_delete.creator:
                    Notification.objects.create(
                        from_user=event_to_delete.creator,
                        to_user=user,
                        title="Event Deleted",
                        description="The event " + event_to_delete.title + " that you were participating in was deleted",
                        url="/events"
                    )

            # delete the event
            event_to_delete.delete()

            return redirect("events:list")
        return HttpResponseForbidden("You are not allowed to delete this event")

    return HttpResponseNotAllowed(["POST"])



@login_required
def load_availability(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)

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
def save_availability(request, event_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    print("Request body:", request.body)
    event = get_object_or_404(Event, event_id=event_id)
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
