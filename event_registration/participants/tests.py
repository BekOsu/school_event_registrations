from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from events.models import Event, EventRegistration, Participant
from django.utils import timezone
from datetime import timedelta


class ParticipantTestCase(TestCase):
    def setUp(self):
        super().setUp()
        future_date_time = timezone.now() + timedelta(days=1)
        self.user = User.objects.create_user(username='john', email='john@example.com', password='johnpassword')
        self.event = Event.objects.create(name="Test Event",
                                          max_participants=5,
                                          date_time=future_date_time
                                          )

    def test_participant_create_view(self):
        self.client.login(username='john', email='john@example.com', password='johnpassword')

        url = reverse('participant_register',
                      kwargs={'event_id': self.event.id})  # Replace with the correct url name
        response = self.client.post(url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone_number': '1234567890',
            # Add other fields as necessary
        })

        self.assertEqual(response.status_code, 302)  # Assuming a successful submission redirects
        self.assertTrue(EventRegistration.objects.filter(event=self.event, participant__user=self.user).exists())

    def test_user_event_list_view(self):
        self.client.login(username='john', email='john@example.com', password='johnpassword')

        participant = Participant.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone_number='1234567890'
        )

        EventRegistration.objects.create(event=self.event, participant=participant)

        url = reverse('events_list')  # Replace with the correct url name
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.event, list(response.context['events']))
