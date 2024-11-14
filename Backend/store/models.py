from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext as _
from django.utils.text import slugify
from django.core.validators import MinValueValidator

from .managers import OrderManager



class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.CharField(max_length=255, blank=True, verbose_name=_("Description"))
    top_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True ,verbose_name=_("Top Product"), related_name='top_product')
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
    
    def __str__(self):
        return self.title


class Discount(models.Model):
    discount = models.FloatField(verbose_name=_("Discount"))
    description = models.CharField(max_length=255, verbose_name=_("Description"))
    # related_name product_set
    
    def __str__(self):
        return f"{self.discount}% off"
    
    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")



class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    slug = models.SlugField(unique=True, db_index=True, blank=True, null=True, verbose_name=_("Slug"))
    category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL, verbose_name=_("Category"), related_name='products')
    description = models.TextField(verbose_name=_("Description"))
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Price"), validators=[MinValueValidator(1)])
    inventory = models.PositiveBigIntegerField(verbose_name=_("Inventory"))
    discounts = models.ManyToManyField('Discount', blank=True ,verbose_name=_("Discounts"), related_name='products')
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Created"))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"))

    def clean(self):
        errors = {}

        if len(self.name) < 1:
            errors['name'] = _('Name must be at least 1 character long.')

        if self.slug and ' ' in self.slug:
            errors['slug'] = _('Slug cannot contain spaces.')

        if len(self.description) < 5:
            errors['description'] = _('Description must be at least 5 characters long.')

        if self.price is None or self.price <= 0:
            errors['price'] = _('Price must be greater than zero.')
        elif self.price >= 10000:
            errors['price'] = _('Price cannot exceed 9999.99.')

        if self.inventory is None or self.inventory < 0:
            errors['inventory'] = _('Inventory cannot be negative.')

        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.full_clean()    
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            
            while Product.objects.filter(slug=slug).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"

            self.slug = slug
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
    
    def __str__(self):
        return self.name



class Customer(models.Model):
    first_name = models.CharField(max_length=255, verbose_name=_("First Name")) # just blank=True
    last_name = models.CharField(max_length=255, verbose_name=_("Last Name"))
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    phone_number = models.CharField(max_length=13, unique=True, verbose_name=_("Phone Number"))
    birth_date = models.DateField(null=True, blank=True,  verbose_name=_("Birth Date"))

    class Meta:
        verbose_name = _('مشتری')
        verbose_name_plural = _('مشتریان')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Order(models.Model):
    ORDER_STATUS_PAIDED = 'p'
    ORDER_STATUS_UNPAIDED = 'u'
    ORDER_STATUS_CANCELLED = 'c'
    
    ORDER_STATUS = (
        (ORDER_STATUS_PAIDED,  _('Paid')),
        (ORDER_STATUS_UNPAIDED,  _('UnPaid')),
        (ORDER_STATUS_CANCELLED,  _('Cancelled')),
    )
    
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name=_("Customer"), related_name='orders')
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Created"))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"))
    status = models.CharField(max_length=255, choices=ORDER_STATUS, default=ORDER_STATUS_UNPAIDED, verbose_name=_("Order Status"))
    
    objects = models.Manager()
    
    order_manager = OrderManager()
    
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
    
    @property
    def customer_name(self):
        return self.customer.first_name
    
    def __str__(self):
        return self.customer.first_name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name=_("Order"), related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_("Product"), related_name='order_items')
    quantity = models.PositiveSmallIntegerField(verbose_name=_("Quantity"))
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Price"))
    
    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')
        
        
    def __str__(self):
        return self.order.customer.first_name


class Comment(models.Model):
    
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'n'
    
    COMMENT_STATUS = (
        (COMMENT_STATUS_WAITING,  _('Waiting')),
        (COMMENT_STATUS_APPROVED,  _('Approved')),
        (COMMENT_STATUS_NOT_APPROVED,  _('Not Approved')),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"), related_name='comments')
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    body = models.CharField(max_length=500, verbose_name=_("Body"))
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Created"))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"))
    status = models.CharField(max_length=13, default=COMMENT_STATUS_NOT_APPROVED , verbose_name=_("Comment Status"))
    
    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
    
    
    def __str__(self):
        return self.name

# id 1 | customer 10 | province: Tehran | city: Tehran | street: Shahre Khani | house_number: 1234
class Addresses(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True,verbose_name=_("Customer")) # Model Customer add filed address
    province = models.CharField(max_length=255, verbose_name=_("Province"))
    city = models.CharField(max_length=255, verbose_name=_("City"))
    street = models.CharField(max_length=255, verbose_name=_("Street"))
    house_number = models.CharField(max_length=255, verbose_name=_("House Number"))
    
    class Meta:
        # db_table = "customer_address"
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
    
    def __str__(self):
        return self.customer.first_name
    
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created_at'))
    
    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
        

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name=_('Cart'), related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'), related_name='cart_items')
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'))
    
    class Meta:
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')
        unique_together = [['cart', 'product']]