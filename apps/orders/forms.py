from django import forms
from .models import PaymentType

# Choice_payment=((1,"Pay through Bank Portal"),(2,"Pay the cost at your place"))                               # (value,description)

# mishod form ham inja nasazim va dar front(html) dar input, value ro {{}} bezarim
class OrderForm(forms.Form):  
    name=forms.CharField(label="",                                                                             # label va input hast
                         widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Name"}),
                         error_messages={"required":"Can not be empty"}
                        )
    
    family=forms.CharField(label="",
                         widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Family"}),
                         required=False
                        )
    
    email=forms.CharField(label="",
                         widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"Email"}),
                         required=False
                        )
    
    phone_number=forms.CharField(label="",
                         widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Phone Number"}),
                         required=False
                        )
    
    address=forms.CharField(label="",
                         widget=forms.Textarea(attrs={"class":"form-control","placeholder":"address","rows":"2"}),
                         error_messages={"required":"Can not be empty"}
                        )
    
    description=forms.CharField(label="",
                         widget=forms.Textarea(attrs={"class":"form-control","placeholder":"description","rows":"4"}),
                         error_messages={"required":"Can not be empty"},
                         required=False
                        )
    
    payment_type=forms.ChoiceField(label="",
                       # choices=Choice_payment,
                         widget=forms.RadioSelect(),
                         choices=[(item.pk,item) for item in PaymentType.objects.all()],                # item miyad __str__ PaymentType ro miyare. item.id=item.pk                          
                        )