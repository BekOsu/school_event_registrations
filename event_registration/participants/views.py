from django.views.generic.edit import CreateView
from django.views import generic
from django.utils import timezone
from events.models import Participant, Event, EventRegistration
from .forms import ParticipantForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse


class ParticipantCreateView(CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'participants/register_participant.html'

    def form_valid(self, form):
        event_id = self.request.POST.get('event', None)

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return HttpResponse("Event does not exist.")

        if event.participants.count() >= event.max_participants:
            return HttpResponse("The event has reached its maximum number of participants.")

        self.object = form.save()
        EventRegistration.objects.create(event=event, participant=self.object)

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
