from django.shortcuts import render
from django.utils import timezone

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import BusyTime
from .forms import BusyTimeForm

# Create your views here.

# @login_required
# TODO: Clean up route
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

    return render(request, 'schedules/busy_times.html', {
        'form': form,
        'busy_times': busy_times,
    })

# @login_required
def availability_calendar(request, event_id):
    context = {
        "event_id": event_id,
        "today": timezone.now().date(),
    }
    return render(request, "schedules/schedule.html", context)

