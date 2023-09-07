from django.views.generic import CreateView, DetailView, ListView, FormView
from django.urls import reverse_lazy
from .fillters import filter_by_type, filter_by_specific_date, filter_by_date_range
from .forms import EventForm, CSVUploadForm
from .models import Event
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .services import parse_csv


class EventFormMixin:
    def handle_event_form(self, form):
        form.instance.created_by = self.request.user
        self.object = form.save()  # Explicitly set self.object after saving the form
        messages.success(self.request, 'Event created successfully.')


class CSVFormMixin:
    def handle_csv_form(self, form):
        csv_file = form.cleaned_data.get('csv_file')

        imported_events = parse_csv(csv_file, self.request)

        for event in imported_events:
            event.created_by = self.request.user
            event.save()

        if imported_events:
            self.object = imported_events[-1]

        messages.success(self.request, 'Events imported successfully.')


class CombinedEventCreateAndCSVImportView(LoginRequiredMixin, EventFormMixin, CSVFormMixin, CreateView, FormView):
    form_class = EventForm
    second_form_class = CSVUploadForm
    template_name = 'events/create_or_import_events.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='EventAdmins').exists():
            raise PermissionDenied("You do not have permission to create or import events.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['csv_form'] = self.second_form_class()
        return context

    def post(self, request, *args, **kwargs):
        if 'event_form' in request.POST:
            self.form_class = EventForm
            return CreateView.post(self, request, *args, **kwargs)
        elif 'csv_form' in request.POST:
            self.form_class = CSVUploadForm
            return FormView.post(self, request, *args, **kwargs)

    def form_valid(self, form):
        if isinstance(form, EventForm):
            self.handle_event_form(form)
            return CreateView.form_valid(self, form)
        elif isinstance(form, CSVUploadForm):
            self.handle_csv_form(form)
            return FormView.form_valid(self, form)

    def get_success_url(self):
        return reverse_lazy('events_list')

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error processing the form.')
        return super().form_invalid(form)


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.object
        return context


@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache for 15 minutes
class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    ordering = ['date_time']

    def get_queryset(self):
        queryset = super().get_queryset().order_by('date_time')

        # Retrieve filtering parameters from GET request
        event_type = self.request.GET.get('event_type')
        event_date = self.request.GET.get('event_date')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        # Apply type filter to queryset
        queryset = filter_by_type(queryset, event_type)

        # If a specific date is provided, filter by that date;
        # otherwise, consider the date range
        if event_date:
            queryset = filter_by_specific_date(queryset, event_date)
        else:
            queryset = filter_by_date_range(queryset, start_date, end_date)

        return queryset
