from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from apps.products.models import Product

# coupon takhfife fardi hast ke dar checkout emal mishe
class Coupon(models.Model):
    coupon_code=models.CharField(max_length=10,unique=True, verbose_name="Cupon code")
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    discount=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    is_active=models.BooleanField(default=False)
    
    class Meta:
        verbose_name: "coupons"
        verbose_name_plural: "coupon"


    def __str__(self):
        return self.coupon_code
    
#-----------------------------------------------------------------------------
# discountBasket yek takhfife omomi hast ke dar shop cart ya birun emal mishe
class DiscountBasket(models.Model):
    discount_title=models.CharField(max_length=50)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    discount=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    is_active=models.BooleanField(default=False)
    
    class Meta:
        verbose_name: "discount_basket"
        verbose_name_plural: "discount_baskets"


    def __str__(self):
        return self.discount_title
    
#-----------------------------------------------------------------------------
# bejaye discountBasketDetail mishod yek field dar product be esme discountBasket ijad kard, ya to discountBasket yek manytomany zad, ya kare zir ro kard
class DiscountBasketDetail(models.Model):               
    discount_basket=models.ForeignKey("discountBasket", on_delete=models.CASCADE, related_name="discountBasket_details")
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_discountDetails")
    
    class Meta:
        verbose_name: "discount_basket_detail"
        verbose_name_plural: "discount_basket_details"

