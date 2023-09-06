from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Event


class EventForm(forms.ModelForm):
    date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Event
        fields = ['name', 'date_time', 'location', 'description', 'max_participants', 'image']

    def clean_date_time(self):
        date_time = self.cleaned_data.get('date_time')
        if not date_time:
            raise forms.ValidationError("This field cannot be empty")
        if date_time <= timezone.now():
            raise forms.ValidationError("The date and time must be in the future")
        return date_time


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file containing event details.'
    )

    def clean_csv_file(self):
        file = self.cleaned_data.get('csv_file')

        if file:
            if not file.name.endswith('.csv'):
                raise forms.ValidationError('This is not a CSV file.')

        return file
