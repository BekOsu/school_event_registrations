from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from events.fillters import filter_by_type, filter_by_specific_date, filter_by_date_range
from events.models import Participant, Event, EventRegistration
from .forms import ParticipantForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from events.tasks import send_event_registration_email


class ParticipantCreateView(LoginRequiredMixin, CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'participants/register_participant.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs.get('event_id')
        event = get_object_or_404(Event, id=event_id)
        context['event'] = event
        return context

    def form_valid(self, form):
        event_id = self.kwargs.get('event_id')
        event = get_object_or_404(Event, id=event_id)

        try:
            participant = Participant.objects.get(user=self.request.user)
        except Participant.DoesNotExist:
            participant = None

        if participant is None:
            new_email = form.cleaned_data['email']
            if Participant.objects.filter(email=new_email).exists():
                messages.error(self.request, "This email is already in use.")
                return self.form_invalid(form)

            participant = Participant(user=self.request.user)

        # Populate or update the Participant record
        participant.first_name = form.cleaned_data['first_name']
        participant.last_name = form.cleaned_data['last_name']
        participant.email = form.cleaned_data['email']
        participant.phone_number = form.cleaned_data['phone_number']
        participant.profile_picture = form.cleaned_data['profile_picture']
        participant.save()

        # Check if the user has already registered for this event
        if EventRegistration.objects.filter(event=event, participant=participant).exists():
            messages.error(self.request, "You have already registered for this event.")
            return self.form_invalid(form)

        # Check maximum participants
        if event.remaining_participants <= 0:
            messages.error(self.request, "The event has reached its maximum number of participants.")
            return self.form_invalid(form)

        # Create the Event Registration
        EventRegistration.objects.create(event=event, participant=participant)

        # Success message
        messages.success(self.request, f"You have been registered for the event: {event.name}.")

        send_event_registration_email.delay(self.request.user.id, event.name)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('user_events')


class UserEventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'participants/participant_event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        user = self.request.user
        try:
            self.participant = Participant.objects.get(user=user)
            queryset = Event.objects.filter(participants=self.participant)
        except ObjectDoesNotExist:
            self.participant = None
            queryset = Event.objects.none()

        event_type = self.request.GET.get('event_type')
        event_date = self.request.GET.get('event_date')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        queryset = filter_by_type(queryset, event_type)

        if event_date:
            queryset = filter_by_specific_date(queryset, event_date)
        else:
            queryset = filter_by_date_range(queryset, start_date, end_date)

        return queryset.order_by('date_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            participant = Participant.objects.get(user=user)
            context['participant'] = participant
        except Participant.DoesNotExist:
            context['participant'] = None
        context['user'] = user
        return context
