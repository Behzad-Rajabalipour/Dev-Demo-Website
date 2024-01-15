from django.shortcuts import render,redirect
from django.views import View
from .forms import RegisterUserForm, VerifyRegisterForm, LoginUserForm, ChangePasswordForm, SendCodeForm, AuthCodeForm, UpdateProfileForm
from .models import CustomUser, Customer
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
import utils
from apps.orders.models import Order
from apps.payments.models import Payment
from django.contrib.auth.decorators import login_required


# to view process anjam mishe

#=====================================================================================
# register
class RegisterUserView(View):
    template_name="accounts_app/register.html"
    
    def dispatch(self, request, *args, **kwargs):                               
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):                    # templates get mikone az inja
        form=RegisterUserForm()
        return render(request,self.template_name,{"form":form})
        
    def post(self, request, *args, **kwargs):                   # templates post mikone be inja
        form=RegisterUserForm(request.POST)
        
        if form.is_valid():
            data=form.cleaned_data
            active_code= utils.create_random_code(5)
            CustomUser.objects.create_user(
                mobile_number=data["mobile_number"],
                active_code=active_code,
                password=data["password1"]
            )
            utils.send_sms(data["mobile_number"],f"you activation code is {active_code}")           # baraye user sms mire
                                                                                
            request.session["user_session"]={                                   # session ha fazayi dar server budan ke mitunestim data tosh zakhire konim. sakhte session be esme user_session
                "active_code":str(active_code),
                "mobile_number":data["mobile_number"]
            }
            
            messages.success(request,"Your information is saved. Please enter activation code","success")
            return redirect("accounts:verify")                                  # inja mibarash safheye Verify baraye vared kardane active_code
        messages.error(request,"Input data is not correct","danger")
        return render(request,self.template_name,{"form":form})

#-------------------------------------------------------------------------------  
class VerifyRegisterCodeView(View):
    template_name="accounts_app/verify_register.html"
    
    def dispatch(self, request, *args, **kwargs):                               
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form=VerifyRegisterForm()
        return render(request,self.template_name,{"form":form})
    
    def post(self, request, *args, **kwargs):
        form=VerifyRegisterForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user_session=request.session["user_session"]                                        # data dakhele session ro inja estefade mikonim. dige lazem nist data ro berim az db biyarim
            if data["active_code"]==user_session["active_code"]:
                user=CustomUser.objects.get(mobile_number=user_session["mobile_number"]) 
                user.is_active=True
                user.active_code=utils.create_random_code(5)                                    # vaghti True shod active_code esh ro avaz kon
                user.save()
                messages.success(request,"You are registered","success")
                return redirect("main:index")
            else:
                messages.error(request,"activation code is wrong","danger")
                return render(request,self.template_name,{"form":form})        # form ba data dakhelesh baz neshun dade mishe
        
        messages.error(request,"Data is not valid","success")
        return render(request,self.template_name,{"form":form})   
                
#=====================================================================================
#login

class LoginUserView(View):
    template_name="accounts_app/login.html"
    
    def dispatch(self, request, *args, **kwargs):            # method dispatch ghabl az har method dige (get,post) ejra mishe. darim migim age user authenticated bud safheye login ro neshun nade
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form=LoginUserForm()
        return render(request,"accounts_app/login.html",{"form":form})

    def post(self, request, *args, **kwargs):
        form=LoginUserForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(username=data["mobile_number"],password=data["password"])                      # authenticate user ro peyda mikone bar migardune. authenticate age user is_active bud bar migardune
            if user is not None:
                db_user=CustomUser.objects.get(mobile_number=data["mobile_number"])
                if db_user.is_admin==False:
                    messages.success(request,"Login is successfull","success")
                    login(request,user)                                                                  # login
                    next_url=request.GET.get("next")                                                     # next. hamun request["next"] hast
                    if next_url is not None:
                        return redirect(next_url)
                    else:
                        return redirect("main:index")
                else:
                    messages.error(request,"admin user can not login from here","danger")
                    return render(request,self.template_name,{"form":form})
            else:
                messages.error(request,"Information is not correct","danger")
                return render(request,self.template_name,{"form":form})
            
        messages.error(request,"Information is not valid","danger")
        return render(request,self.template_name,{"form":form})
        
        
class LogoutUserView(View):
    def dispatch(self, request, *args, **kwargs):                               
        if request.user.is_authenticated==False:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        shop_cart=request.session.get("shop_cart")                              #ref1
        logout(request)                                                             # logout
        request.session["shop_cart"]=shop_cart                                  #ref1, baraye ine ke vaghti logout mikonim shop_cart khali nashe
        messages.success(request,"Logout successfully","success")
        return redirect("main:index")
    
#=====================================================================================
# Forget Password
#step2
class ChangePasswordView(View):
    template_name="accounts_app/change_password.html"
    
    def get(self, request, *args, **kwargs):
        type=kwargs['type']                             # ba type moshakhas mikonim kodom template baz beshe
        if type==1:
            template='user_panel_template.html'
        else: 
            template='main_template.html'
        
        form=ChangePasswordForm()  
        return render(request,self.template_name,{"form":form,'template':template})
    
    def post(self, request, *args, **kwargs):
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            try:                    # In halate Forget Password hast. to in halate session sakhte mishe.
                request.session["user_session"]          
                user_session=request.session["user_session"]
                user=CustomUser.objects.get(mobile_number=user_session["mobile_number"])
            except:                 # In halate dar account, change Password hast. To in halat user login hast va session sakhte nashode 
                user=CustomUser.objects.get(id=request.user.id)
            
            user.set_password(data["password1"])
            user.active_code=utils.create_random_code(5)
            user.save()
            messages.success(request,"Password has been changed","success")
            
            try: 
                request.session["user_session"]          
                return redirect("accounts:login")
            except:
                return redirect("accounts:userpanel")
        
        else:
            messages.error(request,"Input is wrong","danger")
            return render(request,self.template_name,{"form":form})
        
#-----------------------------------------------------------------------------------
#step1
class SendCodeView(View):
    template_name="accounts_app/SendCode.html"
    
    def get(self, request, *args, **kwargs):
        form=SendCodeForm()
        return render(request,self.template_name,{"form":form})
    
    def post(self, request, *args, **kwargs):
        form=SendCodeForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            try:
                user=CustomUser.objects.get(mobile_number=data["mobile_number"])                    # try except, chon age user ro peyda nakone error mide
                active_code=utils.create_random_code(5)
                user.active_code=active_code
                user.save()
                utils.send_sms(data["mobile_number"],f"your activation code is {active_code}")
            
                request.session["user_session"]={                                   
                "active_code":str(active_code),
                "mobile_number":data["mobile_number"]
                }
                messages.success(request,"Enter your code here","success")
                return redirect("accounts:AuthCode")
            
            except:
                messages.error(request,"This mobile number is not exists","danger")
                return render(request,self.template_name,{"form":form})
        
class AuthCodeView(View):
    template_name="accounts_app/AuthCode.html"
    
    def get(self, request, *args, **kwargs):
        form=AuthCodeForm()
        return render (request,self.template_name,{"form":form})
    
    def post(self, request, *args, **kwargs):
        form=AuthCodeForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user_session=request.session["user_session"]                            # un 2 ta data ro to user.session darim
            if data["active_code"]==user_session["active_code"]:
                return redirect("accounts:change_password", "0")                    # dade 0 ro mifrestim ba redirect               
        
            messages.error(request,"Code is wrong","danger")
            form=AuthCodeForm()                                                     # form ro khali kon behesh neshun bede
            return render(request,self.template_name,{"form":form})


#=====================================================================================
class UserPanelView(LoginRequiredMixin,View):                                   # LoginRequiredMixin = user bayad login bashe ta in page baz beshe. age login nabashi mibarat be page login
    def get(self,request):
        user=request.user
        try:
            customer=Customer.objects.get(user=request.user)                        # age customer shode
            user_info={
                "name":user.name,
                "family":user.family,
                "email":user.email,
                "phone_number":customer.phone_number,
                "address":customer.address,
                "image":customer.image_name,
            }
        except:
            user_info={                                                         # age hanuz customer nashode, etelaate useresh ro bebar
                "name":user.name,
                "family":user.family,
                "email":user.email,
            }
        return render(request,"accounts_app/userpanel.html", {"user_info":user_info})

#-----------------------------------------------------------------------------------
@login_required                                                                 # baraye def injuri login required minevisim
def show_last_orders(request):
    orders=Order.objects.filter(customer=request.user.id).order_by("-register_date")[:4]
    return render(request,"accounts_app/partials/show_last_orders.html", {"orders":orders})
    
#-----------------------------------------------------------------------------------
class UpdateProfileView(LoginRequiredMixin,View):
    def get(self,request):
        user=request.user
        try:
            customer=Customer.objects.get(user=request.user)                        
            user_info={
                "mobile_number":user.mobile_number,
                "name":user.name,
                "family":user.family,
                "email":user.email,
                "phone_number":customer.phone_number,
                "address":customer.address,
            }
        except:
            user_info={                                                         
                "name":user.name,
                "family":user.family,
                "email":user.email,
            }
        
        form=UpdateProfileForm(initial=user_info)                                    # formi ke por hast ro mifreste. faghat name to form ba "name" to user_info bayad yeki bashe
        return render(request,"accounts_app/update_profile.html", {"form":form,"image_url":customer.image_name})
    
    def post(self,request):
        form=UpdateProfileForm(request.POST,request.FILES)
        
        if form.is_valid():
            cd=form.cleaned_data
            user=request.user
            user.name=cd['name']
            user.family=cd['family']
            user.email=cd['email']
            user.save()
            try:
                customer=Customer.objects.get(user=request.user)
                customer.phone_number=cd['phone_number']
                customer.address=cd['address']
                if cd['image']:
                    customer.image_name=cd['image']
                customer.save()
            except:
                Customer.objects.create(
                    user=request.user,
                    phone_number=cd['phone_number'],
                    address=cd['address'],
                    image_name=cd['image']
                )    
            messages.success(request,'edit is done','success')
            return redirect("accounts:userpanel")
        
        else:
            messages.error(request,'data is not valid','danger')
            return render("accounts_app/update_profile.html",{'form':form})
            
#-----------------------------------------------------------------------------------
@login_required
def show_user_payments(request):
    payments=Payment.objects.filter(customer_id=request.user.id).order_by('-register_date')
    return render(request,"accounts_app/show_user_payments.html", {"payments":payments})
        