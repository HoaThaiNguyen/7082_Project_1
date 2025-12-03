from django.shortcuts import render
from . import models
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.shortcuts import get_object_or_404
from . import models


@login_required
@require_GET
def get_notifications(request):
    notifications = models.Notification.objects.values(
        'id', 'title', 'description', 'is_read', 'type',
        'from_user__username', 'to_user__username', 'date', 'url'
    ).filter(to_user = request.user).order_by('-date')

    return JsonResponse(list(notifications), safe=False)


@login_required
@require_http_methods(["DELETE"])
def clear_notifications(request):
    models.Notification.objects.filter(to_user=request.user).delete()
    return JsonResponse({"success": True})


@login_required
@require_GET
def has_unread_notifications(request):
    # any user not logged in returns false
    if not request.user.is_authenticated:
        return JsonResponse({'has_unread': False})
    
    # return if one or more notifications unread exist for logged in user
    at_least_one_unread = models.Notification.objects.filter(
        to_user=request.user,
        is_read=False
    ).exists()
    return JsonResponse({'has_unread': at_least_one_unread})


@login_required
@require_POST
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(models.Notification, id=notification_id)

    if notification.to_user != request.user:
        return JsonResponse({'error': "Not allowed to change notifications other than your own"}, status=403)
    
    notification.is_read = True
    notification.save()

    return JsonResponse({'success': True})

# TODO: 
# - if have time, perhaps clean up the code a little (instead of /events, do event:events or something, also replace with django template code where possible)