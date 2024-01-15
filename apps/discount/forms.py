from django import forms

class CouponForm(forms.Form):
    coupon_code=forms.CharField(label="",
                                widget=forms.TextInput(attrs=({"class":"form-control","placeholder":"coupon code"})),
                                error_messages={"required":"This filed can not left emplt"}
                                )