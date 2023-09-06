from django import forms
from events.models import Participant


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_picture']
