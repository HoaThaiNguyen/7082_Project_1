from django.shortcuts import render
from .models import Event

# Create your views here.
def events(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'events/events.html', {'events': events})