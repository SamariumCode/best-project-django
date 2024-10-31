from django.contrib import admin
from django.utils.translation import gettext as _
from django.utils.html import format_html


from .models import Product, Customer, Category, Order, Comment, Discount, OrderItem, Addresses, Cart, CartItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_category', 'description_words', 'price', 'inventory', 'inventory_status']
    list_per_page = 20
    list_editable = ('price', 'inventory')
    list_select_related = ['category']
    
    # def short_description(self, product):
    #     description_words = product.description.split()[:5]
    #     return ' '.join(description_words) + ('...' if len(product.description.split()) > 5 else '')
    
    @admin.display(ordering='category__title')
    def product_category(self, product):
        return product.category.title if product.category else None
    
    product_category.short_description = _('Product category')
    
    
    def description_words(self, product):
        return  product.description[:20] + "..." if product.description and len(product.description) > 20 else product.description
    
    description_words.short_description =  _('Product Description')
    
    @admin.display(ordering='inventory')
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

    
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'body_words', 'status', 'datetime_created', 'datetime_modified']
    list_editable = ['status']
    list_per_page = 10
    # list_select_related = ['product']
    
    def body_words(self, comment):
        return  comment.body[:50] + "..." if comment.body and len(comment.body) > 50 else comment.body

    body_words.short_description = _('Comment Body')
    

# Register all models
# admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Order)
# admin.site.register(Comment)
admin.site.register(Discount)
admin.site.register(OrderItem)
admin.site.register(Addresses)
admin.site.register(Cart)
admin.site.register(CartItem)

