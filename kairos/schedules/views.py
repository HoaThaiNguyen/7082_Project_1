from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
import json

from .models import BusyTime
from .forms import BusyTimeForm

# Create your views here.

# @login_required
def busy_times_view(request):
    user = request.user
    busy_times = BusyTime.objects.filter(user=user).order_by('day_of_week', 'start_time')
    
    if request.method == 'POST':
        form = BusyTimeForm(request.POST)
        if form.is_valid():
            busy_time = form.save(commit=False)
            busy_time.user = user
            busy_time.save()
            return redirect('busy_times')
    else:
        form = BusyTimeForm()

    events = [
        {
            "title": busy.description or "Busy",
            "daysOfWeek": [(busy.day_of_week+1)%7],
            "startTime": str(busy.start_time),
            "endTime": str(busy.end_time),
        }
        for busy in busy_times
    ]

    context = {
        "form": BusyTimeForm(),
        "busy_times": busy_times,
        "events_json": json.dumps(events, cls=DjangoJSONEncoder),
    }
    return render(request, "schedules/busy_times.html", context)

# # @login_required
# def busy_times_view(request):
#     user = request.user
#     busy_times = BusyTime.objects.filter(user=user).order_by('day_of_week', 'start_time')

#     if request.method == 'POST':
#         form = BusyTimeForm(request.POST)
#         if form.is_valid():
#             busy_time = form.save(commit=False)
#             busy_time.user = user
#             busy_time.save()
#             return redirect('busy_times')
#     else:
#         form = BusyTimeForm()

#     return render(request, 'schedules/busy_times.html', {
#         'form': form,
#         'busy_times': busy_times,
#     })
