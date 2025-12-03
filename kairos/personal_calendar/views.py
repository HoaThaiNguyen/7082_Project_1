from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
import json

from .models import RecurringBusyTime
from .forms import RecurringBusyTimeForm

# Create your views here.

# @login_required
def personal_calendar_view(request):
    user = request.user
    recurring_busy_times = RecurringBusyTime.objects.filter(user=user).order_by('day_of_week', 'start_time')
    
    if request.method == 'POST':
        form = RecurringBusyTimeForm(request.POST)
        if form.is_valid():
            recurring_busy_time = form.save(commit=False)
            recurring_busy_time.user = user
            recurring_busy_time.save()
            return redirect('personal_calendar:personal_calendar')
    else:
        form = RecurringBusyTimeForm()

    # Serialize recurring busy times for JS editing
    recurring_busy_times_json = json.dumps([
        {
            "pk": b.pk,
            "day_of_week": b.day_of_week,
            "start_time": b.start_time.strftime("%H:%M"),
            "end_time": b.end_time.strftime("%H:%M"),
            "description": b.description,
        }
        for b in recurring_busy_times
    ], cls=DjangoJSONEncoder)

    # For right-side Calendar events
    events = [
        {
            "title": recurring_busy_time.description or "Busy",
            "daysOfWeek": [(recurring_busy_time.day_of_week+1)%7],
            "startTime": str(recurring_busy_time.start_time),
            "endTime": str(recurring_busy_time.end_time),
        }
        for recurring_busy_time in recurring_busy_times
    ]

    context = {
        "form": RecurringBusyTimeForm(),
        "recurring_busy_times": recurring_busy_times,
        "events_json": json.dumps(events, cls=DjangoJSONEncoder),
    }
    return render(request, "personal_calendar/personal_calendar.html", context)


def edit_recurring_time(request, pk):
    busy_time = get_object_or_404(RecurringBusyTime, pk=pk)
    if request.method == "POST":
        form = RecurringBusyTimeForm(request.POST, instance=busy_time)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    return redirect('personal_calendar:personal_calendar')


def delete_recurring_time(request, pk):
    if request.method == "POST":
        recurring_time = get_object_or_404(RecurringBusyTime, pk=pk)
        recurring_time.delete()
    return redirect('personal_calendar:personal_calendar')

