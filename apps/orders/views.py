from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .shop_cart import ShopCart                 # . yani hamin address
from apps.products.models import Product
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order,OrderDetail,PaymentType
from apps.accounts.models import Customer
from .forms import OrderForm
from apps.discount.forms import CouponForm
from django.db.models import Q
from apps.discount.forms import CouponForm
from apps.discount.models import Coupon
from datetime import datetime
from django.contrib import messages
import utils

#-----------------------------------------------------
class ShopCartView(View):                       # chop shop cart yek safheye kamel hast pas class barash minevisim
    def get(self, request, *args, **kwargs):
        shop_cart=ShopCart(request)             
        return render(request,"orders_app/shop_cart.html",{"shop_cart":shop_cart})

#-----------------------------------------------------
def add_to_shop_cart(request):
    product_id=request.GET.get("product_id")
    qty=request.GET.get("qty")
    color = request.GET.get("color")
    
    shop_cart=ShopCart(request)
    product=get_object_or_404(Product, id=product_id)
    shop_cart.add_to_shop_cart(product,qty,color)
    return HttpResponse(shop_cart.count)

#-----------------------------------------------------
def delete_from_shop_cart(request):
    product_id=request.GET.get("product_id")
    product=get_object_or_404(Product,id=product_id)
    shop_cart=ShopCart(request)
    shop_cart.delete_from_shop_cart(product)
    return redirect("orders:show_shop_cart")                            # baes mishe vaghti delete mikoni safhe dade jadid ro neshun bede

#-----------------------------------------------------
def show_shop_cart(request):
    shop_cart=ShopCart(request)
    total_price=shop_cart.calc_total_price()
    
    order_final_price,delivery,tax=utils.price_by_delivery_tax(total_price)
    
    context={
        "shop_cart":shop_cart,
        "shop_cart_count":shop_cart.count,
        "total_price":total_price,
        "delivery":delivery,
        "tax":tax,
        "order_final_price":order_final_price
    }
    return render(request,"orders_app/partials/show_shop_cart.html", context)

#-----------------------------------------------------
def update_shop_cart(request):
    product_id_list=request.GET.getlist("product_id_list[]")             # age query string list bud bayad injuri get konim
    qty_list=request.GET.getlist("qty_list[]")                           # index 1 dar product_id_list marbot be inedx 1 dar qty_list hast
    shop_cart=ShopCart(request)
    shop_cart.update(product_id_list,qty_list)
    return redirect("orders:show_shop_cart")

#-----------------------------------------------------
def status_of_shop_cart(request):
    shop_cart=ShopCart(request)
    return HttpResponse(shop_cart.count)

#-----------------------------------------------------
# sabt dar db
class CreateOrderView(LoginRequiredMixin,View):                         # agar in fun farakahni shod va Login nabod mibaratesh be safheye Login
    def get(self,request):
        try:
            customer=get_object_or_404(Customer,user=request.user)         # request ba khodeh user ro ham miyare. # age customer nabod besaz    
        except:
            customer=Customer.objects.create(user=request.user)         # chon momkene user bashe vali hanuz Customer nashode bashe
        
        order=Order.objects.create(customer=customer,payment_type=get_object_or_404(PaymentType,id=1))      # hardafe order misaze. nemishod bedim payment_type=1
        
        shop_cart=ShopCart(request)                                 # shop_cart dakhelesh por hast
        for item in shop_cart:                                      # baraye har item shop_cart yek order_detail besaz
            OrderDetail.objects.create(
                order=order,
                product=item["product"],
                qty=item["qty"],
                price=item["price"]
            )
            
        return redirect("orders:checkout_order", order.id,"None")                  # param ba khodesh mibare, coupon="None"
    
#-----------------------------------------------------
# namayeshe checkout
class CheckOutOrderView(LoginRequiredMixin,View):
    def get(self,request,order_id,coupon_code):                                                 
        user=request.user
        customer=get_object_or_404(Customer,user=request.user)
        shop_cart=ShopCart(request)
        
        order=get_object_or_404(Order,id=order_id)
        if coupon_code:
            coupon_code=coupon_code
        else:
            coupon_code="None"
        
        total_price=shop_cart.calc_total_price()
        order_final_price,delivery,tax=utils.price_by_delivery_tax(total_price, order.discount)             # order.discount = in ghesmat dar button apply dar front emal mishe. discount 2/2
        
        data={
            "name":user.name,
            "family":user.family,
            "email":user.email,
            "phone_number":customer.phone_number,
            "address":customer.address,
            "description":order.description,
            "payment_type":order.payment_type,
        }
        
        form=OrderForm(data)                            # form ba data ersal mishe. form baraye front(UI) hast
        form_coupon=CouponForm()
        
        context={
            "shop_cart":shop_cart,
            "shop_cart_count":shop_cart.count,
            "total_price":total_price,
            "delivery":delivery,
            "order":order,
            "tax":tax,
            "order_final_price":order_final_price,
            "form":form,
            "form_coupon":form_coupon,
            "user.name":user.name,                       # age mikhastim form nasazimm 
            "coupon_code":coupon_code
        }
        
        # for orderDetail in order.order_Details.all():        # tamame oderDetail haye in order ro miyare
        #     print(orderDetail.product.product_name)
        # print(order)
        
        return render(request,"orders_app/checkout.html", context)

    # update information to db va ersal be dargahe pardakht
    def post(self,request,order_id,coupon_code):
        form=OrderForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            try:
                order=Order.objects.get(id=order_id)
                order.description=cd["description"]
                order.payment_type=PaymentType.objects.get(id=cd["payment_type"]) 
                order.save()
                
                user=request.user
                user.name=cd['name']
                user.family=cd["family"]
                user.email=cd["email"]
                user.save()
                
                customer=Customer.objects.get(user=request.user)
                customer.phone_number=cd["phone_number"]
                customer.address=cd["address"]
                customer.save()
                
                return redirect("payments:zarinpal_payment", order_id)                      # redirect mikone be dargahe zarinpal
            except:
                messages.error(request,"order does not found","danger")
                return redirect("orders:checkout_order", order_id,"None")
        return redirect("orders:checkout_order", order_id,"None") 
                
#-----------------------------------------------------
# verify coupon_code. rikhtane discounte Coupon model toye discounte Order model 
# #ref5 Product model, discount 2/2
class ApplyCoupon(View):                                        
    def post(self,request,*args,**kwargs):                           # az front be sorate post ferestadim inja
        order_id=kwargs["order_id"]
        coupon_form=CouponForm(request.POST)
        if coupon_form.is_valid():
            cd=coupon_form.cleaned_data
            coupon_code=cd["coupon_code"]
            
        coupon=Coupon.objects.filter(                                   # begard to Coupon object ha
            Q(coupon_code=coupon_code) &
            Q(is_active=True) &
            Q(start_date__lte=datetime.now()) &                         # __lte
            Q(end_date__gte=datetime.now())                             # __gte
        )
        
        discount=0
        try:
            order=Order.objects.get(id=order_id)
            if coupon:
                discount=coupon[0].discount      
                order.discount=discount
                order.save()
                
                messages.success(request,"coupon applied","success")
                return redirect("orders:checkout_order", order_id,coupon_code)
            else:
                order.discount=discount
                order.save()
                messages.error(request,"coupon does not found","danger")
                return redirect("orders:checkout_order", order_id,"None")
        except:
            messages.error(request,"order does not found","danger")
            return redirect("orders:checkout_order", order_id,"None")
        
            
            