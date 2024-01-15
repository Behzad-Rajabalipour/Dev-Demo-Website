from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Product,ProductGroup,FeatureValue,Brand
from django.db.models import Q, Count, Max, Min,Case,When,IntegerField,Sum
from django.views import View        
from django.http import JsonResponse
from .filters import ProductFilter
from django.core.paginator import Paginator
from .compare import CompareProduct

# 1. pip install django-render-partial
# 2. settings => INSTALLED_APPS = []  => 'django_render_partial'
# 3. optional : templates => main_app => index.html => {% load render_partial %} => {% render_partial 'main:test_view' %} 
# 4. optional: urls => tarif kardane url barash

# ba module "render_partial" mishe chandta functione view ro dar 1 safheye html ejra konim
# agar az module "render_partial" estefade nakonim bayad hameye etelaat ro to yek functione view berizim
# "render_partial" => index.html aval mire view ro mikhune.

#------------------------------------------------------------------------------------
def get_cheapest_products(request, *args, **kwargs):
    products=Product.objects.filter(is_active=True).order_by("price")[:5]                         # filter bar khalafe get(1 item) list bar migardune
    product_groups=ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))          # age bekhaym chandta filter dashte bashim az Q estefade mikonim
    context={
        "products":products,
        "product_groups": product_groups
    }
    return render(request,"products_app/partials/cheapest_products.html",context)

#------------------------------------------------------------------------------------
def get_most_purchased_products(request,*args,**kwargs):
    products = Product.objects.filter(
        Q(is_active=True) & ~Q(product_warehouses=None)
    ).annotate(                                                 # anotate() is just for filter
        sellQty=Sum(                        # when we say Sum, it means te object is iterable
            Case(                           # for each Sum() we can have only one Case()
                When(product_warehouses__warehouse_type__warehouse_type_title="sell", then='product_warehouses__qty'),   # when is condition. with __ we deep into the next model
                default=0,
                output_field=IntegerField()
            )
        )
    ).order_by('-sellQty')[:6]              # order_by works just with filter() function
    
    return render(request,"products_app/partials/most_purchased_products.html",{"products":products})

#------------------------------------------------------------------------------------
def get_last_products(request, *args, **kwargs):
    products=Product.objects.filter(is_active=True).order_by("-published_date")[:5]                       # - naghize
    product_groups=ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))
    context={
        "products":products,
        "product_groups":product_groups
    }
    
    if not kwargs["widget"]:
        return render(request,"products_app/partials/last_products.html",context)
    else:
        return render(request,"products_app/partials/widget_last_products.html",context)        
        
        

#------------------------------------------------------------------------------------
def get_popular_productGroups(request, *args, **kwargs):                                          # ba \ mitunim beshkanim line ro
    product_groups=ProductGroup.objects.filter(is_active=True)\
                                                .annotate(count=Count("products_of_group"))\
                                                .order_by("-count")[:4]
    return render(request,"products_app/partials/popular_productGroups.html",{"product_groups":product_groups})

#------------------------------------------------------------------------------------
class ProductDetailView(View):                                                                  # class get va post dare
    def get(self,request,slug):
        product=get_object_or_404(Product, slug=slug)                                           # model Product ba in slug ro miyare ya error 404 mide
        if product.is_active:
            return render(request,"products_app/product_detail.html",{"product":product})

# vaghti partial bashe ba def va vaghti to yek safhe joda bashe ba class minevisim
#------------------------------------------------------------------------------------
def get_related_products(request,*args,**kwargs):                                                                 # hameye product hayi ke product_group yeki daran
    current_product=get_object_or_404(Product,slug=kwargs["slug"])
    realated_products=[]
    for group in current_product.product_group.all():
        realated_products.extend(Product.objects.filter(Q(is_active=True) & Q(product_group=group) & ~Q(id=current_product.id)))          # ~Q naghize. baraye inke khodet product ro dobare nayare
    return render(request,"products_app/partials/related_products.html",{"related_products":realated_products})  

#------------------------------------------------------------------------------------
class ProductGroupsView(View):
    def get(self,request):
        product_groups=ProductGroup.objects.annotate(count=Count("products_of_group"))\
                                                .filter(Q(is_active=True) & ~Q(count=0))\
                                                .order_by("-count")                                             # - naghize, yani Desc
        return render(request,"products_app/product_groups.html",{"product_groups":product_groups})

#------------------------------------------------------------------------------------
def get_product_groups(request):
    product_groups=ProductGroup.objects.annotate(count=Count("products_of_group"))\
                                            .filter(Q(is_active=True) & ~Q(count=0))\
                                            .order_by("-count")                                             # - naghize, yani Desc
    print(product_groups)
    
    return render(request,"products_app/partials/product_groups.html",{"product_groups":product_groups})


#------------------------------------------------------------------------------------
class ProductsOfGroup(View):
    def get(self,request,*args,**kwargs):
        current_group=get_object_or_404(ProductGroup,slug=kwargs['slug'])
        products=Product.objects.filter(Q(is_active=True) & Q(product_group=current_group))                     # current_group.id ham doroste
        
        #-----------------
        # max va min input Price
        res_aggre=products.aggregate(min=Min("price"), max=Max("price"))                              # res_aggre = {min:Min("price"), max:Max("price")}. min,max,count,avg
        
        #-----------------
        # filter 1
        # pip install django-filter => INSTALLED_APPS = ['django_filters'] => create filters.py
        filter=ProductFilter(request.GET, queryset=products)
        products=filter.qs                                     # qs = query set.  products filter 1. baraye filtere price
        
        #-----------------
        # filter 2
        brands_filter=request.GET.getlist("brand")              # age to url list omad ba getlist migirim. masalan liste brand
        if brands_filter:
            products=products.filter(brand__id__in=brands_filter)       # products filter 2. baraye filtere brands. chon list hast pas in mizarim
        
        #-----------------
        # filter 3
        features_filter=request.GET.getlist("featureValue")             # baraye filtere featureValue 
        if features_filter:
            products=products.filter(product_features__filter_value__id__in=features_filter).distinct()            # value haye un feature va feature haye un product. value gheyre tekrari bar migardune. distinct() age tekrari bashe nemiyare
        
        #-----------------
        # sort
        sort_type=request.GET.get("sort_type")
        if not sort_type:
            sort_type="0"
        if sort_type=="1":
            products=products.order_by("price")
        if sort_type=="2":
            products=products.order_by("-price")

        #-----------------
        # pager
        group_slug=kwargs["slug"]
        products_per_page=request.GET.get("productsPerPage")
        
        if not products_per_page:
            products_per_page=3
        else:
            products_per_page=int(products_per_page)
        
        paginator=Paginator(products,products_per_page)          # we input all products and products per page
        current_page=request.GET.get("page", 1)                     # this comes from from URl based on GET method
        current_page = int(current_page)                        # it must be int otherwise in front we can not use i == current_page 
        
        page_obj=paginator.get_page(current_page)                # page_obj is three products obj in for example page=2 
        
        page_numbers = range(1, paginator.num_pages + 1)
        
        product_count=products.count()
                
        #-----------------
        show_count_product=[]
        i=3
        while i<product_count:
            show_count_product.append(i)
            i*=2
        show_count_product.append(i)
        
        #-----------------
        # price
        price=request.GET.get("price")
        #-----------------
        # context
        context={
            "products":products,
            "current_group":current_group,
            "current_page":current_page,
            "page_numbers":page_numbers,
            "res_aggre":res_aggre,
            "group_slug":group_slug,
            "page_obj":page_obj,
            "product_count":product_count,
            "show_count_product":show_count_product,
            "products_per_page":products_per_page,
            "filter":filter,                        # filter ro ham bayad bebarim front
            "sort_type":sort_type,
            "price":price,
            }
        
        return render(request,"products_app/products_of_group.html",context)

#------------------------------------------------------------------------------------
# two dropdown in ProductAdmin panel
def get_filter_value_for_feature(request):
    if request.method == "GET":
        feature_id=request.GET["feature_id"]
        feature_values=FeatureValue.objects.filter(feature_id=feature_id)
        res={fv.value_title:fv.id for fv in feature_values}
        return JsonResponse(data=res)                       # bar migardune be ajax (file admin_script)
    
#------------------------------------------------------------------------------------
def get_brands(request,*args,**kwargs):
    product_group = get_object_or_404(ProductGroup, slug=kwargs["slug"])

    # Annotate each brand with the count of products in the specified product group
    brands = Brand.objects.filter(                  # brands = [brand1, brand2, brand3, ...]
        products_brand__product_group=product_group,
        products_brand__is_active=True
    ).annotate(                             # annotate means add a field to each brand. brand1.products_brand=[product1, product2, product3, ...]
        count=Count(                        # Count means Iterable. Add 1 ro count if product_group of each product equal to product_group
            Case(
                When(products_brand__product_group=product_group, then=1),
                output_field=IntegerField()
            )
        )
    ).filter(
        count__gt=0                 # gt means greate than
    ).order_by('-count')
    
    return render(request, "products_app/partials/brands.html", {"brands":brands})

#------------------------------------------------------------------------------------
# feature ha ba value hashun
def get_features_for_filter(request, *args, **kwargs):
    product_group=get_object_or_404(ProductGroup,slug=kwargs["slug"])
    features_list=product_group.features_of_group.all()
    feature_dict=dict()
    for feature in features_list:
        feature_dict[feature]=feature.feature_values.all()                              # {feature1: [value1, value2, value3], feature2: [value2, value]}
    
    return render(request, "products_app/partials/features_filter.html",{"feature_dict":feature_dict})

#------------------------------------------------------------------------------------
# compare products. kole safhe
class showCompareListViw(View):                         # class neveshtim chon kole safhe ro migire. age bakhshi az safhe bud def mineveshtim
    def get(self,request,*args,**kwarsg):
        return render(request,'products_app/compare_list.html')    

#------------------------------------------------------------------------------------
# compare product dakhele div
def compare_table(request):
    compareList=CompareProduct(request)                        # yek object ke iter hast bar migardune. kole session omad to compare_list
    
    products=[]
    for productId in compareList:
        product=Product.objects.get(id=productId)              
        products.append(product)
        
    features=[]
    for product in products:
        for ProductFeature in product.product_features.all():                                # ManyToMany. Product => ProductFeature(table) => product_features. ProductFeature haro miyare
            if ProductFeature.feature not in features:                                             
                features.append(ProductFeature.feature)
        
    context={
        'products':products,
        'features': features
    }
    
    return render(request,'products_app/partials/compare_table.html',context)

#------------------------------------------------------------------------------------
def add_to_compare_list(request):
    productId=request.GET.get("productId")
    # productGroupId=request.GET["productGroupId"]                  # in baraye ine ke age productha bar asase groheshun baham moghayese beshan. masaln pofak ba laptop moghayese nashe
    compareList=CompareProduct(request)                             
    compareList.add_to_compare_product(productId)
    return HttpResponse("product added to compare list")
    
#------------------------------------------------------------------------------------
# count ro bar migardun
def status_of_compare_list(request):
    compareList=CompareProduct(request)
    return HttpResponse(compareList.count)

#------------------------------------------------------------------------------------
def delete_from_compare_list(request):
    productId=request.GET.get("productId")
    compareList=CompareProduct(request)                             
    compareList.delete_from_compare_product(productId)
    return redirect("products:compare_table")                               # resi ke be ajax bar migarde in redirect tosh hast
