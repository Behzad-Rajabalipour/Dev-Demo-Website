from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,UserManager         # agar User ro negah koni mibini farzande AbstractUser hast. AbstractUser az ghabl koli property va method mesle is_active, get_full_name,first_name va ... dare
from django.utils import timezone
from utils import FileUpload
from uuid import uuid4

# model data base hast

# inharo az file text اپلیکیشن avordam

#       (موبایل) مدل کاربر:
#        رمز عبور
#        ایمیل
#        نام
#        نام خانوادگی
#        جنسیت
#        تاریخ ثبت نام
#        وضعیت کاربر(فعال/غیر فعال)
#        کد فعال سازی
#        وضعیت ادمین(هست/نیست)
	

# ============================part 2

# in class be vasilye class CustomUser miyad User ya SuperUser ro misaze. 
# def create_user() and create_superuser() ke dar class UserManager hastan ro dobare nevisi mikonim
class CustomUserManager(UserManager):
    def create_user(self, mobile_number,password,email="",name="",family="",active_code=None,gender=None):      # email,name,family mitune baraye user adi khali bashe vali chon ejbariye nemishe None gozasht
        if not mobile_number:
            raise ValueError("Mobile number must be inserted")
        
        user=self.model(                                    # yek model misaze
            mobile_number=mobile_number,
            email=email,
            name=name,
            family=family,
            active_code=active_code,
            gender=gender
        )
        
        user.set_password(password)                         # hash mikone password ro, to classe UserManager injuri neveshte= make_password(password)  
        user.save(using=self._db)                           # to db save mikone, using ro age naneveshtim ham okeye
        return user
        
    def create_superuser(self, mobile_number,password,email,name,family,active_code=None,gender=None):
        user=self.create_user(
            mobile_number=mobile_number,
            email=email,
            name=name,
            family=family,
            active_code=active_code,
            gender=gender,
            password=password
        )
        user.is_active=True
        user.is_admin=True
        user.is_superuser=True
        user.save()
        return user
    
# ============================part 1

# in modele User ma hast, in modele paye hast ke CustomUserManager() rosh run mishe
class CustomUser(AbstractBaseUser,PermissionsMixin):                                     
    mobile_number=models.CharField(max_length=11,unique=True, verbose_name="Mobile Number")
    email=models.EmailField(max_length=200,blank=True)          # chon null=True nadare to db bayad por beshe
    name=models.CharField(max_length=50,blank=True)
    family=models.CharField(max_length=50,blank=True)
    gender=models.CharField(max_length=50,choices=(("True","Male"),("False","Female")),default="True",null=True,blank=True)         # True ya False barmigardune, Male ya Female to UI neshun mide
    register_date=models.DateField(default=timezone.now)
    is_active=models.BooleanField(default=False)
    active_code=models.CharField(max_length=100,blank=True,null=True)
    is_admin=models.BooleanField(default=False)
    
    #--------------------------------
    # in baraye sakhte user dar shell hast
    # in 2 line baes mishe CustomUser jaye User ke default hast ro begire. password ro ham khodesh mizare ro in filedha                           
    # settings => AUTH_USER_MODEL="accounts.CustomUser"   ro bayad ezafe konim
    USERNAME_FIELD="mobile_number"                            
    REQUIRED_FIELDS=["email","name","family"]                 
    
    objects=CustomUserManager()                         # inja behesh migim CustomUserManager() ro to in model save kon, hatman bayad objects injuri bashe
    
    #--------------------------------
    def __str__(self):
        return self.name+" "+self.family
    
    #---------------------------------
    
    @property                           # ba in decorator is_staff ro az def be property taghir dadim
    def is_staff(self):                 # in True bar migardune age user admin bashe. in property ro dobare nevisi kardim
        return self.is_admin
    
    #---------------------------------


# ============================part 3
# in model dar modele apps.orders karbord dare
class Customer(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)                 # chon one to one hast pas jofteshun Unique hastan. masalan inja user 3 connect be onvar user 3 
    phone_number=models.CharField(max_length=11,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    file_upload=FileUpload("images","customer")
    image_name=models.ImageField(upload_to=file_upload.upload_to,null=True,blank=True)
    
    
    def __str__(self):
        return f"{self.user}"                                                           # to admin mire __str__ self.user ro miyare