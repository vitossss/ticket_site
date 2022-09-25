from rest_framework import views, status
from rest_framework.response import Response

from .models import Ticket, Payment, Order, OrderItem
from .serializers import TicketSerializer


class TicketView(views.APIView):
    def get(self, request, ticket_slug=None):
        if not ticket_slug:
            tickets = Ticket.objects.all()
            serializer = TicketSerializer(tickets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            ticket = Ticket.objects.get(slug=ticket_slug)
            serializer = TicketSerializer(ticket, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
