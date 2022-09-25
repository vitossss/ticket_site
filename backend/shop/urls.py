from django.urls import path
from .views import TicketView

urlpatterns = [
    path('tickets/', TicketView.as_view()),
    path('tickets/<slug:ticket_slug>/', TicketView.as_view()),
]
