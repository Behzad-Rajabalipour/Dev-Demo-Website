from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# form front kar hast

class UserCreationForm(forms.ModelForm):                    
    password1=forms.CharField(label="Password",widget=forms.PasswordInput)
    password2=forms.CharField(label="RePassword",widget=forms.PasswordInput)
    
    class Meta:                                             # harvaght MoedlForm dashtim bayad class Meta dashte bashim
        model=CustomUser
        fields=["mobile_number","email","name","family","gender"]

    def clean_password2(self):                              # def clean(self) baraye hameye filedha mishe, def clean_email(self) baraye check email hast 
        pass1=self.cleaned_data["password1"]
        pass2=self.cleaned_data["password2"]
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("Passwords are not matched")
        return True
    
    def save(self,commit=True):                            
        user=super().save(commit=False)                     # def save() joze def haye class ModelForm hast. Inja baz nevisish mikonim chon mikhaym aval save nakone, pass ro hash kone bad save kone
        user.set_password(self.cleaned_data["password1"])   
        user.save()                                         # user.save(commit=True) ham mishe
        return user
    
#--------------------------------------------------------------------------    
class UserChangeForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField(help_text="For changing the Password <a href='../password'>click</a> here")                    # in baes mishe password be sorate hash to form be karbar neshun bede. variable password ro khodesh dare
    
    class Meta:
        model=CustomUser
        fields=["mobile_number","password","email","name","family","gender","is_active","is_admin"]

#--------------------------------------------------------------------------    
class RegisterUserForm(forms.ModelForm):
    class Meta:
        model=CustomUser            
        fields=["mobile_number","name","family","email"]                                    # label bayad to model verbose_name behesh bedi
        widgets={                                                   # chon class Meta hast injuri widgets midim
            "mobile_number":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Mobile Number"}),
            "name":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Your Name"}),
            "family":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Your Family"}),
            "email":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Your Email"})
        }    
    password1=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter your Password"}))
    password2=forms.CharField(label="Repeat Password",widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter your Repeat Password"}))
    
    def clean_password2(self):                            
        pass1=self.cleaned_data["password1"]
        pass2=self.cleaned_data["password2"]
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("Passwords are not matched")
        return True

#--------------------------------------------------------------------------    
class VerifyRegisterForm(forms.Form):
    active_code=forms.CharField(label="",
                                error_messages={"required":"this field can not left empty"},
                                widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter activation code"})        # widget baraye har field
                                )

#==========================================================================================
# Login
class LoginUserForm(forms.Form):
    mobile_number=forms.CharField(label="Mobile Number",
                                  error_messages={"required":"this field can not left empty"},
                                  widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Mobile"}))
    password=forms.CharField(label="Password",
                                error_messages={"required":"this field can not left empty"},
                                widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter password"})        
                                )

#=====================================================================================
# Forget Password
class ChangePasswordForm(forms.Form):
    password1=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter your Password"}))
    password2=forms.CharField(label="Repeat Password",widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter your Repeat Password"}))

    def clean_password2(self):                            
        pass1=self.cleaned_data["password1"]
        pass2=self.cleaned_data["password2"]
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("Passwords are not matched")
        return True
    
    
class SendCodeForm(forms.Form):
    mobile_number=forms.CharField(label="Mobile Number",
                                  error_messages={"required":"this field can not left empty"},
                                  widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Mobile"}))
    
class AuthCodeForm(forms.Form):
    active_code=forms.CharField(label="Active Code",
                                  error_messages={"required":"this field can not left empty"},
                                  widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter active code"}))

#=====================================================================================
class UpdateProfileForm(forms.Form):
    mobile_number=forms.CharField(label="",
                                  widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Mobile","readonly":"readonly"}))        # readonly bashe
    
    name=forms.CharField(label="",
                                  error_messages={'required':"this field can not be empty"},
                                  widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Name"}))
    
    family=forms.CharField(label="",
                                  error_messages={'required':"this field can not be empty"},
                                  widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Family"}))
    
    email=forms.CharField(label="",
                                  error_messages={'required':"this field can not be empty"},
                                  widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"Enter Email"}))
    
    phone_number=forms.CharField(label="",
                                  error_messages={'required':"this field can not be empty"},
                                  widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Phone Number"}))
    
    address=forms.CharField(label="",
                                  error_messages={'required':"this field can not be empty"},
                                  widget=forms.Textarea(attrs={"class":"form-control","placeholder":"Enter Address"}))
    
    image=forms.ImageField(required=False)
    