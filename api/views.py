from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from events.models import Event
from .serializers import EventSerializer
from .permissions import IsCreator


class PublicEventsView(APIView):
    queryset = Event.objects.filter(is_public=True)
    serializer_class = EventSerializer

    def get(self, request):
        serializer = self.serializer_class(self.queryset.all(), many=True)
        return Response(serializer.data)


class UserEventsView(APIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Event.objects.filter(creator=user)
        return queryset

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)


class EventView(RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsCreator]
