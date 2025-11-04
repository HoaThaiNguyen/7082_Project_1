from django.shortcuts import render
from .models import Event
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# Create your views here.
def events(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'events/events.html', {'events': events})


def user_events(request):
    user = request.user
    events = user.event_set.all().values('id', 'name', 'date')
    return Response({'events': list(events)})
