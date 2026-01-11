from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ticket', 'quantity', 'total_amount', 'status')
    list_filter = ('status',)
    search_fields = ('user__email', 'id')