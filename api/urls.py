from django.urls import path
from .views import PublicEventsView, UserEventsView, EventView

urlpatterns = [
    path('public_events/', PublicEventsView.as_view(), name='public_event'),
    path('events/', UserEventsView.as_view(), name='user_events'),
    path('events/<int:pk>/', EventView.as_view(), name='event_detail'),
]