from django.db import models
from django.conf import settings
import uuid
# We import the Ticket model to link them
from tickets.models import Ticket 

class Order(models.Model):
    """
    Order model to track ticket purchases.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Link to the User who bought it
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    # Link to the Ticket they bought
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='orders')
    
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {str(self.id)[:8]} - {self.user}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate total price
        if not self.total_amount:
            self.total_amount = self.ticket.price * self.quantity
        super().save(*args, **kwargs)