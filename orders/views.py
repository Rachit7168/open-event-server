from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # 1. Save the order
        # We assume the user is the one logged in
        order = serializer.save(user=self.request.user)
        
        # 2. Update the Ticket Inventory
        ticket = order.ticket
        ticket.quantity -= order.quantity
        ticket.save()