from django.db import models
from django.contrib.auth.models import User  # or use get_user_model()
# (see note below)

class NotificationType(models.TextChoices):
    EVENT_INFO = 'INFO', 'Event Info'
    WARNING = 'WARN', 'Warning'
    ERROR = 'ERR', 'Error'


class Notification(models.Model):
    type = models.CharField(
        max_length=10,
        choices=NotificationType.choices,
        default=NotificationType.EVENT_INFO,
    )

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    url = models.URLField(max_length=500, default="http://localhost:8000/events", help_text="URL to redirect the user when they click this notification")
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    from_user = models.ForeignKey(
        User,
        related_name='sent_notifications',
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User,
        related_name='received_notifications',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"[{self.type}] {self.title}"