from django.urls import path
from .views import ParticipantCreateView, EventListView

urlpatterns = [

    path('register/', ParticipantCreateView.as_view(), name='participant_register'),
    path('events/', EventListView.as_view(), name='event_list'),

]
