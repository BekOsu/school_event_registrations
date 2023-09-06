from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.views import generic
from django.utils import timezone
from events.models import Participant, Event, EventRegistration
from .forms import ParticipantForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages


class ParticipantCreateView(CreateView):
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

        if event.remaining_participants <= 0:
            messages.error(self.request, "The event has reached its maximum number of participants.")
            return self.form_invalid(form)

        participant = form.save()
        EventRegistration.objects.create(event=event, participant=participant)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('event_list')


class EventListView(generic.ListView):
    model = Event
    context_object_name = 'events'
    template_name = 'events/event_list.html'

    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '')
        if filter_val:
            return Event.objects.filter(
                # Implement your filtering logic here.
                # For example, for filtering by date:
                date_time__gte=timezone.now(),
                date_time__date=filter_val,
            ).order_by('date_time')
        else:
            return Event.objects.filter(
                date_time__gte=timezone.now()
            ).order_by('date_time')
