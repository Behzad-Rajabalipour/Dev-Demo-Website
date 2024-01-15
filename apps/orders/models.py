from django.db import models
from django.utils import timezone
from apps.accounts.models import Customer
from apps.products.models import Product
from uuid import uuid4
import utils

# -----------------------------------------------------------
class PaymentType(models.Model):
    payment_title=models.CharField(max_length=50)
    
    def __str__(self):
        return self.payment_title
    
# -----------------------------------------------------------
class OrderState(models.Model):
    order_state_title= models.CharField(max_length=50)
    
    def __str__(self):
        return self.order_state_title
    
    class Meta:
        verbose_name="order state"
        verbose_name_plural="order states"
        
# -----------------------------------------------------------
# har bar ke to Front clicke edameye kharid bezanim yek Order sabt mishe
class Order(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_orders")
    register_date=models.DateField(default=timezone.now)
    update_date=models.DateField(auto_now=True)
    is_finaly=models.BooleanField(default=False)
    order_date=models.UUIDField(unique=True, default=uuid4, editable=False)
    discount=models.IntegerField(blank=True, null=True, default=0)                          # null: default=None
    #----------------------------
    # ezafe kardam in field haro be model. field hayi ke dafe 2vom ezafe mishan be model hatman bayad null=True, blank=True bashe
    description=models.TextField(blank=True, null=True)
    payment_type=models.ForeignKey("PaymentType",default=None ,on_delete=models.CASCADE, blank=True, null=True)
    order_state=models.ForeignKey(OrderState, on_delete=models.CASCADE, null=True, blank=True)              # chon in field badan ezafe shode hatam bayad null va blank bezari
    #----------------------------
    
    def get_order_total_price(self):
        total_price=0
        for item in self.order_Details.all():
            total_price+=item.product.get_price_by_discount()*item.qty              # total_price ro inja az db avordim na az shop_cart

        order_final_price,delivery,tax=utils.price_by_delivery_tax(total_price, self.discount)
        
        return int(order_final_price)
    
    def __str__(self):
        return f"{self.customer}\t{self.id}\t{self.is_finaly}\t{self.order_Details.all()}"
    
    class Meta:
        verbose_name="order"
        verbose_name_plural="orders"
        
# -----------------------------------------------------------
# joziyate un order ro mibare db
class OrderDetail(models.Model):
    order=models.ForeignKey(Order, verbose_name="Order", on_delete=models.CASCADE, related_name="order_Details")
    product=models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE, related_name="product_details")
    qty=models.PositiveIntegerField(default=1)
    price=models.IntegerField(verbose_name="price of item")
    
    def __str__(self):
        return f"{self.order}\t{self.product}\t{self.qty}\t{self.price}"