from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.orders.models import Order, OrderState
from apps.payments.models import Payment
from apps.accounts.models import Customer
from apps.warehouses.models import Warehouse, WarehouseType
from django.http import HttpResponse
import requests
import json

# etelaate in safhe az zarinpal miyad(API) bad man edit va ezafe kardam behesh => www.zarinpal.com/lab/نمونه-درگاه-زرین-پال-python-تحت-فریم-ورک-django
# in module ro az website zarinpal migirim, bad editesh mikonim
# baraye test API va tarakonesh: 
# 1. az dargahe majazi => https://banktest.ir/   yek account mikharim
# 2. etelaate zir ro avaz mikonim be dargahe majazi
MERCHANT = 'A4F1193A-BD47-41AC-905D-568010285301'                   # in line ro bad az sabtenam dar zarinpal behemun mide
ZP_API_REQUEST = "https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://sandbox.banktest.ir/zarinpal/www.zarinpal.com/pg/StartPay/{authority}"

CallbackURL = 'http://127.0.0.1:8000/payments/verify/'                       # tarjihan localhost ro pak kon va 127.0.0.1 benevis

# module zir ro ke az site zarinpal gereftim edit mikonim
#-----------------------------------------------------------------------------------
# send mikone be dargahe zarinpal
class ZarinpalPaymentSend(LoginRequiredMixin,View):                 # send   
    def get(self,request, order_id):
        try:
            order=Order.objects.get(id=order_id)
            
            payment=Payment.objects.create(
                order=order,
                customer= Customer.objects.get(user=request.user),
                amount= order.get_order_total_price(),
                description= "Payment Through Zarinpal Gate",
            )
            payment.save()            
            
            request.session['payment_session']={
                'order_id':order.id,
                'payment_id':payment.id
            }
            user=request.user
            req_data = {                                             # in code ro az zarinpal miyarim
            "merchant_id": MERCHANT,                                 # in code unique hast ke zarinpal bade sabtenam mide
            "amount": order.get_order_total_price(),                 # dade haro az shop_cart nuemikhunim chon amn nist. az db mikhunim
            "callback_url": CallbackURL,
            "description": "Payment Through Zarinpal Gate",
            "metadata": {"mobile": user.mobile_number, "email": user.email}
            }
            req_header = {"accept": "application/json", "content-type": "application/json'"}            # code zarinpal
            req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)      # code zarinpal
            authority = req.json()['data']['authority']                                                 # code zarinpal. age accounte banktest.ir nadashte bashim inja error mmide
            
            if len(req.json()['errors']) == 0:                                                          # code zarinpal. javab be sorate string miyad, na API(Json), baraye hamin .json mizanim
                return redirect(ZP_API_STARTPAY.format(authority=authority))                            # dobare mifrestim be dargahe zarinpal. format to python un ghesmate "/{authority}" ro por mikone
            else:                                                                                       # code zarinpal. age khata dasht error ro neshun bede
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
        except Exception as err:
            return redirect("orders:checkout_order", order_id,"None")

#-----------------------------------------------------------------------------------
# daryaft mikone az dargahe zarinpal
class ZarinpalPaymentVerify(LoginRequiredMixin,View):                 # verify
    def get(self,request):
        order_id=request.session['payment_session']['order_id']
        payment_id=request.session['payment_session']['payment_id']
        
        order=Order.objects.get(id=order_id)
        payment=Payment.objects.get(id=payment_id)
        
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        if request.GET.get('Status') == 'OK':
            req_header = {"accept": "application/json", "content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": order.get_order_total_price(),
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)       # dobare ersal mishe be zarinpal
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:                                             # status 100 va 101 yani pardakht anjam shode
                    order.is_finaly=True
                    order.order_state=OrderState.objects.get(id=1)
                    order.save()
                    
                    for order_detail in order.order_Details.all():
                        Warehouse.objects.create(
                            warehouse_type=WarehouseType.objects.get(id=2),             # nemituni mostaghim benevisi 2. bayad khode record ro biyari
                            user_registered=request.user,
                            product=order_detail.product,
                            qty=order_detail.qty,
                            price=order_detail.price
                        )
                        
                    payment.is_finally=True
                    payment.status_code=t_status
                    payment.ref_id=str(req.json()['data']['ref_id'])
                    payment.save()

                    request.session['payment_session'] = None
                    request.session["shop_cart"] = None
                    
                    return redirect("payments:show_verify_message", f"Payment is successfull, ref id= {str(req.json()['data']['ref_id'])}")
                elif t_status == 101:
                    order.is_finaly=True
                    order.order_state=OrderState.objects.get(id=1)
                    order.save()
                    
                    payment.is_finally=True
                    payment.status_code=t_status
                    payment.ref_id=str(req.json()['data']['ref_id'])
                    payment.save()
                    
                    for order_detail in order.order_Details.all():
                        Warehouse.objects.create(
                            warehouse_type=WarehouseType.objects.get(id=2),             # nemituni mostaghim benevisi 2. bayad khode record ro biyari
                            user_registered=request.user,
                            product=order_detail.product,
                            qty=order_detail.qty,
                            price=order_detail.price
                        )
                    
                    return redirect("payments:show_verify_message", f"Payment is accepted, ref id= {str(req.json()['data']['ref_id'])}")
                else:
                    payment.status_code=t_status
                    payment.save()
                    
                    return redirect("payments:show_verify_message", f"Payment is Unsuccessfull, status= {t_status}")
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return redirect("payments:show_verify_message", f"Error code: {e_code}, Error Message: {e_message}")
                
        else:
            return redirect("payments:show_verify_message", 'Transaction failed or canceled by user')

#-----------------------------------------------------------------------------

def show_verify_message(request, message):
    return render(request,"payments_app/verify_message.html",{"message":message})