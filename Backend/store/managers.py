from django.db import models

class OrderManager(models.Manager):
    def paid_orders(self):
        from .models import Order
        return self.filter(status=Order.ORDER_STATUS_PAIDED)
    
    def unpaid_orders(self):
        from .models import Order
        return self.filter(status=Order.ORDER_STATUS_UNPAIDED)
    
    def cancelled_orders(self):
        from .models import Order
        return self.filter(status=Order.ORDER_STATUS_CANCELLED)