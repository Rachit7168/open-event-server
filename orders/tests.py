from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from tickets.models import Ticket
from orders.models import Order

User = get_user_model()

class OrderAPITest(TestCase):
    def setUp(self):
        # FIX: We added 'username' here because the User model requires it
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        
        # Create a ticket with 10 in stock
        self.ticket = Ticket.objects.create(
            name='Gold Pass',
            price=50.00,
            quantity=10
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_order_success(self):
        """Test that buying a ticket works and reduces inventory"""
        data = {
            'ticket': self.ticket.id,
            'quantity': 2
        }
        
        response = self.client.post('/v3/orders/', data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        
        # Check inventory dropped
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.quantity, 8)

    def test_create_order_insufficient_stock(self):
        """Test that you cannot buy more tickets than available"""
        data = {
            'ticket': self.ticket.id,
            'quantity': 100
        }
        
        response = self.client.post('/v3/orders/', data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Inventory should NOT change
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.quantity, 10)
