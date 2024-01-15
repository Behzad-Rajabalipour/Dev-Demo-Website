from django.db import models
from apps.orders.models import Order
from apps.accounts.models import Customer
from django.utils import timezone

class Payment(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_payments")
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_payments")
    register_date=models.DateTimeField(default=timezone.now, verbose_name="tarikhe pardakht")
    update_date=models.DateTimeField(auto_now=True, verbose_name="tarikhe virayesh")
    amount=models.IntegerField()
    description=models.TextField()
    is_finally=models.BooleanField(default=False)
    
    status_code=models.IntegerField(null=True,blank=True)
    ref_id=models.CharField(max_length=50,null=True,blank=True)
    
    
    
    def __str__(self):
        return f"{self.order} {self.customer} {self.ref_id}"
    
    class Meta:
        verbose_name="payment"
        verbose_name_plural="payments"