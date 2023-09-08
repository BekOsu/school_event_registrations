from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from events.models import Event, EventRegistration, Participant


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


class UserEventListViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.event = Event.objects.create(name="Test Event", max_participants=5, date_time="2023-09-06 14:30:59")
        self.participant = Participant.objects.create(user=self.user)
        self.event.participants.add(self.participant)

    def test_login_required(self):
        response = self.client.get(reverse('user_events'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_query_set_for_participant(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('user_events'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.event, response.context['events'])

    def test_context_data(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('user_events'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(response.context['participant'], self.participant)
