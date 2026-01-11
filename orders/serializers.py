from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'ticket', 'quantity', 'total_amount', 'status']
        read_only_fields = ['id', 'total_amount', 'status', 'user']

    def validate(self, data):
        """
        Check if enough tickets are available.
        """
        ticket = data['ticket']
        quantity = data['quantity']
        
        if ticket.quantity < quantity:
            raise serializers.ValidationError("Not enough tickets available.")
        
        return data