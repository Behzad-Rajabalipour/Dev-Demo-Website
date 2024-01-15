from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserChangeForm,UserCreationForm
from .models import CustomUser, Customer

class CustomUserAdmin(UserAdmin):                              # bejaye admin.Admin az User userAdmin estefade mikonim
    form = UserChangeForm                                      # form az property khodesh hast, baz nevisi mikonim
    add_form = UserCreationForm                                # add_form az property khodesh hast, baz nevisi mikonim

    list_display=("mobile_number","email","name","family","gender")
    list_filter=("is_active","is_admin","family")
    
    # filedsets va add_fielsets ro dobare nevisi mikonim. ctrl+ UserAdmin
    fieldsets=((None,{"fields":("mobile_number","password")}),                  # avali onvan, savomi esme filed ha
               ("Personal Info",{"fields":("email","name","family","gender","active_code")}),
               ("Permissions",{"fields":("is_active","is_admin","is_superuser","groups","user_permissions")}))
    
    
    add_fieldsets=(
        (None,{"fields":("mobile_number","email","name","family","gender","password1","password2")}),
    )
    
    search_fields=("mobile_number",)
    ordering=("mobile_number",)
    filter_horizontal=("groups","user_permissions")                     # choosen groups va choosen user permission ro ezafe mikone
    
    
admin.site.register(CustomUser,CustomUserAdmin)             # inja register mikone in model ro roye in admin

#---------------------------------------------------------------

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=["user","phone_number"]