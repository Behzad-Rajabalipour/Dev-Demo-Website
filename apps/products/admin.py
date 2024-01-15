from django.contrib import admin
from .models import Brand, ProductGroup, Product, ProductFeature,Feature, ProductGallery, FeatureValue
from django.db.models.aggregates import Count,Max
from django.http import HttpResponse
from django.core import serializers
from django_admin_listfilter_dropdown.filters import DropdownFilter
from django.db.models import Q
from django.contrib.admin import SimpleListFilter
from admin_decorators import short_description, order_field

#========================================================================
class BrandInlineAdmin(admin.TabularInline):
    model=Product

#------------------------------------------
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display=("brand_title","slug","Max_PK_table_2vom")
    list_filter=("brand_title",)                    # chon tuple 1 duneyi hast bayad , bezarim
    search_fields=("brand_title",)
    ordering=("brand_title",)
    inlines=[BrandInlineAdmin]                                  # Foreign Key. admin => add=> Pk table balayi mishe FK table payinini 
    
    def get_queryset(self, *args, **kwargs):
        qs=super(BrandAdmin,self).get_queryset(*args,**kwargs)   
        qs=qs.annotate(MaxProductId=Max("products_brand"))
        return qs
    
    def Max_PK_table_2vom(self,obj):
        return obj.MaxProductId
    
#========================================================================
def deactive_productGroup(modeladmin,request,queryset):             # queryset inja recordhaye select shode dar table hastan
    res=queryset.update(is_active=False)                            # res tedade fieldhayi ke rushun emal shode bar migardune
    message=f"{res} number of Prduct Group is deactivated"
    modeladmin.message_user(request,message)

def active_productGroup(modeladmin,request,queryset):
    res=queryset.update(is_active=True)
    message=f"{res} number of Prduct Group is activated"
    modeladmin.message_user(request,message)
    
def export_json_API(modeladmin,request,queryset):
    response=HttpResponse("application/json")
    serializers.serialize("json", queryset, stream=response)
    return response

#------------------------------------------
class ProductGroupInlineAdmin(admin.TabularInline):                     # refer1
    model=ProductGroup                                                  # hatman bayad Fk dashte bashe
    extra=1
    
#------------------------------------------
# 1. cmd: pip install django-admin-list-filter-dropdown                     # dropdown miyare list_filter ro 
# 2. settings.py => INSTALLED_APPS => "django_admin_listfilter_dropdown"
# 3. from django_admin_listfilter_dropdown.filters import DropdownFilter    # refer2

#------------------------------------------
# Modify kardane filter
class GroupFilter(SimpleListFilter):
    title="Custom Product Group Filter"                                  # filter name
    parameter_name="group"                                               # url 
    
    def lookups(self, request, model_admin):                             #  dobare nevisi mikonim. def SimpleListFilter hast
        Sub_groups=ProductGroup.objects.filter(~Q(group_parent=None))       # ~ alamate naghize
        groups=set([record.group_parent for record in Sub_groups])          # record.group_parent yani kole recode group_parent ro miyare. to groups alan hameye recordhaye ProductGroup hast be joz payin tarin sub group
        return [(record.id,record.group_title) for record in groups]        # refer3. (value, queryset)
    
    def queryset(self, request, queryset):
        if self.value()!=None:                                              # refer3 value hamun record.id hast
            return queryset.filter(Q(group_parent=self.value()))            # to url joloye ?group=value
        return queryset
    
#------------------------------------------
@admin.register(ProductGroup)    
class ProductGroupAdmin(admin.ModelAdmin):
    list_display=("group_title","is_active","group_parent","slug","count_groups","count_products_of_group","display_Products_of_group")
    list_filter=("group_title",("group_parent",DropdownFilter),GroupFilter)                     # refer2            
    search_fields=("group_title",)
    ordering=("group_parent","group_title")
    inlines=[ProductGroupInlineAdmin]                                   # refer1, admin => add => Fk table payini ro mizare Pk table balayi. self join 
    actions=[deactive_productGroup, active_productGroup, export_json_API]
    list_editable=["is_active"]                                         # hatman bayad boolean bedim
    
#------------------------------------------
# in 2ta def payin baraye ezafe kardane fielde jadid hast    
    def get_queryset(self,*args,**kwargs):                              # esme def bayad hamin bashe
        qs=super(ProductGroupAdmin,self).get_queryset(*args,**kwargs)   # qs kole table ba list_display dar admin hast
        qs=qs.annotate(CountGroups=Count("groups",distinct=True))                        # annotate yek field ezafe mikone be qs be esme sub_group. Inja fielde related_name ro gozashtim.
        qs=qs.annotate(CountProductsOfGroup=Count("products_of_group",distinct=True))     # product_group dar Product model
        return qs
    
    def count_groups(self,obj):                                      # obj dakhelesh qs hast. Tedeade PK table 2vom ke Fk zadan
        return obj.CountGroups
        
    count_groups.short_description="Count PK table 2vom or Count sub Group"                      # refer4 raveshe 1val, esme ro to list_display taghir mide. joloye har group(Digi Kala) => tedade sub group ro neshun midad  
    deactive_productGroup.short_description="Deactive Product Group"                             # emse ro to actions taghir mide

#-------------------
# 1. pip install django-admin-decorators
# 2. from admin_decorators import short_description, order_field 
    @short_description("Count Products of this Group")                                           # refer4 raveshe 2vom, 
    @order_field("CountProductsOfGroup")                                                         # admin => list_display => vaghti roye in field click koni order mishe
    def count_products_of_group(self,obj):
        return obj.CountProductsOfGroup
    
#-------------------
    def display_Products_of_group(self,obj):
        return ", ".join([Product.product_name for Product in obj.products_of_group.all()]) 
        
#========================================================================
def deactive_product(modeladmin,request,queryset):             
    res=queryset.update(is_active=False)                            
    message=f"{res} number of Prduct is deactivated"
    modeladmin.message_user(request,message)

def active_product(modeladmin,request,queryset):
    res=queryset.update(is_active=True)
    message=f"{res} number of Prduct is activated"
    modeladmin.message_user(request,message)

#------------------------------------------
class ProductFeatureInlineAdmin(admin.TabularInline):
    model=ProductFeature                                                    # payinesh in table ezafe mishe. Fk table payini(Product dar Table ProductFeature) ro mizare Pk table balayi.
    extra=3
    
    class Media:                                                            # baraye dadan css va js be admin ProductAdmin
        css={
            "all":("css/admin_style.css",)
        }
        js=(
            "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.3/jquery.min.js",
            "js/admin_script.js",
        )
#------------------------------------------
class ProductGalleryInlineAdmin(admin.TabularInline):
    model=ProductGallery                                                    
    extra=3
#------------------------------------------
@admin.register(Product)    
class ProductAdmin(admin.ModelAdmin):
    list_display=("product_name","price","brand","is_active","published_date","slug","display_Product_groups")                  # register_date va update_date chon auto_now_add hastan to admin nemiyan
    list_filter=("brand","product_group")                          
    search_fields=("product_name",)
    ordering=("update_date","product_name")
    actions=[deactive_product,active_product]
    inlines=[ProductFeatureInlineAdmin, ProductGalleryInlineAdmin]                      # ProductFeatureInlineAdmin = many_to_many
    
#------------------------------------------
# column ezafe mikone be list_display
    def display_Product_groups(self,obj):
        return ", ".join([ProductGroup.group_title for ProductGroup in obj.product_group.all()])            # product_group hamun filede dar Product model hast. obj kole recordhaye Product hast.
    
    display_Product_groups.short_description="Product Groups"
    
#------------------------------------------
    def formfield_for_manytomany(self, db_field, request, **kwargs):                                # in def ro dobare nevisi mikonim. Dar ModelAdmin hast.
        if db_field.name=="product_group":                                                          # in yek dune field ro taghir bede bad return kon.
            kwargs["queryset"]=ProductGroup.objects.filter(~Q(group_parent=None))                   # ~ alamate naghize. admin => add Product => product_group => in def baes mishe sar dasteha (group_parent) ro nayare to admin
        return super().formfield_for_manytomany(db_field, request, **kwargs)

#------------------------------------------                
    fieldsets=(
        ("Product Information",{"fields":(
            "product_name",
            "image_name",
            ("product_group","brand","is_active"),                                              # in filed ha ro to yek line miyare
            "price",
            "description",
            "slug"
        )}),
        (
            "Date and Time",{"fields":(
                "published_date",
            )}
        )
    )
        
#========================================================================
class FeatureValueInLine(admin.TabularInline):
    model= FeatureValue
    extra=3
        
#----------------------------
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display=("feature_name","display_groups","display_feature_values" )
    list_filter=("feature_name",)                          
    search_fields=("feature_name",)
    ordering=("feature_name",)
    inlines=[FeatureValueInLine,]
    
    def display_groups(slef,obj):
        return ', '.join([group.group_title for group in obj.product_group.all()])
    
    def display_feature_values(self,obj):
        return ", ".join([value.value_title for value in obj.feature_values.all()])
    
    
    display_groups.short_description="product_groups of this feature"
    display_feature_values.short_description="values of this feature"
#========================================================================

