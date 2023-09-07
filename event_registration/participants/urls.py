from django.urls import path
from . import views

urlpatterns = [

    path('register/<int:event_id>/', views.ParticipantCreateView.as_view(), name='participant_register'),
    path('user_events/', views.UserEventListView.as_view(), name='user_events'),

]
