from django.contrib import admin
from django.utils.translation import gettext as _
from django.utils.html import format_html


from .models import Product, Customer, Category, Order, Comment, Discount, OrderItem, Addresses, Cart, CartItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'description_words', 'price', 'inventory', 'inventory_status']
    list_per_page = 20
    list_editable = ('price', 'inventory')

    
    # def short_description(self, product):
    #     description_words = product.description.split()[:5]
    #     return ' '.join(description_words) + ('...' if len(product.description.split()) > 5 else '')
    
    
    def description_words(self, product):
        return  product.description[:20] + "..." if product.description and len(product.description) > 20 else product.description
        
        
    def inventory_status(self, product):
        max_inventory = 100     
        percentage = round(min(max(product.inventory / max_inventory * 100, 0), 100))

        if percentage <= 10:
            color = 'red'
            status_text = _('Low inventory')
        elif percentage <= 50:
            color = 'orange'
            status_text = _('Medium inventory')
        else:
            color = 'green'
            status_text = _('High inventory')

        return format_html(
            '<div style="width: 100%; background-color: #e0e0e0; border-radius: 5px;">'
            '<div style="width: {}%; background-color: {}; height: 10px; border-radius: 5px;"></div>'
            '</div>'
            '<div style="text-align: center; font-size: 12px;">{} ({}%)</div>',
            percentage, color, status_text, percentage   
        )

    inventory_status.short_description = _('Inventory Status')

    
# Register all models
# admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Comment)
admin.site.register(Discount)
admin.site.register(OrderItem)
admin.site.register(Addresses)
admin.site.register(Cart)
admin.site.register(CartItem)

