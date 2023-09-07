from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from events.models import Participant, Event, EventRegistration
from .forms import ParticipantForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


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

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('events_list')
