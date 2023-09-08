from django.urls import path

from . import views

urlpatterns = [
    path('events_list/', views.EventListView.as_view(), name='events_list'),
    path('create_event/', views.CombinedEventCreateAndCSVImportView.as_view(), name='event_create'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
]
