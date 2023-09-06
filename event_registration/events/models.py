from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class Event(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='events/', default='events/default_image.jpg.png')
    date_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.TextField(max_length=600)
    max_participants = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_time']

    def clean(self):
        if self.date_time is None:
            raise ValidationError("Date and Time are required")
        if self.date_time <= timezone.now():
            raise ValidationError("The date and time must be in the future")

    def was_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_at <= now

    def get_absolute_url(self):
        return reverse('event_detail', args=[str(self.id)])

    def __str__(self):
        return self.name
