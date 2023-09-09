from rest_framework import viewsets, permissions, renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from events.models import Event
from .serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def remaining_participants(self, request, *args, **kwargs):
        event = self.get_object()
        return Response(event.remaining_participants)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
