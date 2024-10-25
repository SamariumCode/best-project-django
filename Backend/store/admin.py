from django.contrib import admin

from .models import Product, Customer, Category, Order, Comment, Discount, OrderItem, Addresses, Cart, CartItem

# Register all models
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Comment)
admin.site.register(Discount)
admin.site.register(OrderItem)
admin.site.register(Addresses)
admin.site.register(Cart)
admin.site.register(CartItem)

