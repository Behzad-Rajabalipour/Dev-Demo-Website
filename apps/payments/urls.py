from django.urls import path
from . import views

app_name="payments"
urlpatterns = [
    path("zarinpal_payment/<int:order_id>/",views.ZarinpalPaymentSend.as_view(),name="zarinpal_payment"),
    path("verify/",views.ZarinpalPaymentVerify.as_view(),name="verify"),
    path("show_verify_message/<str:message>/",views.show_verify_message,name="show_verify_message"),
]
