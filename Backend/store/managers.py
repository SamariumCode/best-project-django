from django.db import models

from .models import Order

class OrderManager(models.Manager):
    def paid_orders(self):
        return self.filter(status=Order.PENDING)
    
    def unpaid_orders(self):
        return self.filter(status=Order.UNPAIDED)
    
    def cancelled_orders(self):
        return self.filter(status=Order.CANCELLED)