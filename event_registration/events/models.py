import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Event(models.Model):

    EVENT_TYPE_CHOICES = (
        ('conference', 'Conference'),
        ('seminar', 'Seminar'),
        ('workshop', 'Workshop'),
        ('webinar', 'Webinar'),
    )

    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='events/', default='default_event.png')
    date_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.TextField(max_length=600)
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES, default='conference')
    max_participants = models.PositiveIntegerField(default=0)
    participants = models.ManyToManyField('Participant', through='EventRegistration', related_name='events')
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

    @property
    def remaining_participants(self):
        return self.max_participants - self.participants.count()

    def __str__(self):
        return self.name


class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default_user.png',  null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if EventRegistration.objects.filter(event=self.event, participant=self.participant).exists():
            raise ValidationError("User is already registered for this event")
        if self.event.remaining_participants <= 0:
            raise ValidationError("The event has reached its maximum number of participants")
        super(EventRegistration, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.event} - {self.participant}"

