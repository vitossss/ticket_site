from rest_framework import serializers
from .models import Ticket, Payment, Order, OrderItem


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        exec = ("creation_time",)
