from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BusyTime(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='busy_times')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}: {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"
