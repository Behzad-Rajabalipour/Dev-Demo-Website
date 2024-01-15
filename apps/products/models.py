from django.db import models
from utils import FileUpload
from django.utils import timezone                                       # cmd: py manage.py check => check mikone error nadashte bashi
from ckeditor.fields import RichTextField                               # faghat text ro upload mikone
from ckeditor_uploader.fields import RichTextUploadingField             # text va file ro upload mikone
from django.urls import reverse
from datetime import datetime
from django.db.models import Sum, Avg
from middlewares.middlewares import RequestMiddleware
from django.db.models.signals import post_delete                        # bade delete yek record image un az server hazf nemishod baraye hamin signals estefade mikonim. model haye digeye signals dar site django models signals  
from django.dispatch import receiver

# az texte application miyarim
        # مدل برند:
	# 	کد برند
	# 	نام برند
#------------------------------------------------------------
class Brand(models.Model):
    brand_title=models.CharField(max_length=100,verbose_name="Brand Title")
    file_upload=FileUpload("images","brands")
    image_name=models.ImageField(upload_to=file_upload.upload_to, verbose_name="Brand Image Name")
    slug=models.SlugField(max_length=200,null=True)
    
    def __str__(self):
        return self.brand_title
    
    class Meta:
        verbose_name="Brand"
        verbose_name_plural="Brands"

#------------------------------------------------------------
	# مدل کالا :
	# 	کد کالا			12		15		
	# 	نام کالا			پیراهن		عسل		
	# 	توضیحات کالا
	# 	نام تصویر اصلی کالا
	# 	-گروه کالا			3		4
	# 	قیمت فروش کالا
	# 	-برند
	# 	وضعیت (فعال/غیر فعال)

def upload_image(instance,filename):
    return f"images/product_group/{filename}"

 
class ProductGroup(models.Model):
    group_title= models.CharField(max_length=100, verbose_name="Group Title")
    file_upload=FileUpload("images","product_group")
    image_name=models.ImageField(upload_to=file_upload.upload_to, verbose_name="ProductGroup Image Name")
    description=models.TextField(blank=True,null=True,verbose_name="Description")
    is_active=models.BooleanField(default=True,blank=True,verbose_name="Is Active")
    group_parent=models.ForeignKey("ProductGroup", on_delete=models.CASCADE,verbose_name="Parent Group", blank=True, null=True, related_name="groups")           # baraye har joini hatman bayad Foreign key dashte bashim. to table aval(ke PK toshe) dar admin yek field be esme groups misaze. dakhele groups PK haye table 2vom ke Fk zadan ro mizare.
    slug=models.SlugField(max_length=200,null=True)
    # product=models.ManyToManyField("Product", related_name="Products")                     # refer2
    # feature= models.ManyToManyField("Feature", related_name="Features")                    # refer3
    
    def __str__(self):
        return self.group_title
    
    class Meta:
        verbose_name="Product Group"
        verbose_name_plural="Products Group"

#------------------------------------------------------------
class Feature(models.Model):
    feature_name=models.CharField(max_length=100,verbose_name="Feature Name")
    product_group=models.ManyToManyField("ProductGroup",verbose_name="Product Group", related_name="features_of_group")   # chon ManytoMany pas product_group=[product_group1, product_group2,...] hast  # refer3, to table ProductGroup dar admin yek field be esme feature_of_group misaze. ke bayad farakhani beshe ta dide beshe.
    # Product=models.ManyToManyField("Product",related_name="Products")
    
    def __str__(self):
        return self.feature_name
    
    class Meta:
        verbose_name="Feature Name"
        verbose_name_plural="Features Name"

#------------------------------------------------------------
class Product(models.Model):
    product_name=models.CharField(max_length=500, verbose_name="Product Name")
    summary_description=models.TextField(default="",null=True,blank=True)
#---------------------------------
#   1. pip install django-ckeditor
#   2. settings => INSTALLED_APPS => add ckeditor, add ckeditor_uploader
#   3. settings => end of the page => ezafe kardane tanzimate ckeditor
#   4. urls asli => path("ckeditor",include("ckeditor_uploader.urls"))
#   5. importe har 2 ta module  
    description= RichTextUploadingField(config_name="special", blank=True)                                                              # mishe configs haye dige ham to settings ezafe kard. to admin taghir mikone.
#---------------------------------
    file_upload=FileUpload("images","product")
    image_name=models.ImageField(upload_to=file_upload.upload_to, verbose_name="Product Image Name")
    price=models.PositiveBigIntegerField(default=0, verbose_name="Price")
    slug=models.SlugField(max_length=200,null=True)
    is_active=models.BooleanField(default=True,blank=True,verbose_name="Is Active")
    register_date=models.DateTimeField(auto_now_add=True)                                                                               # editable nist
    published_date=models.DateTimeField(default=timezone.now)
    update_date=models.DateTimeField(auto_now=True)
    brand=models.ForeignKey("Brand", verbose_name="Brand", on_delete=models.CASCADE, null=True, related_name="products_brand" )                   
    product_group=models.ManyToManyField("ProductGroup", verbose_name="Product Group", related_name="products_of_group")                   # refer2, to db bridge table mizane, to admin filede product_group ro neshun mide. to ProductGroup yek column be esme product_of_group ezafe mishe ke dakhelesh Pk haye record Product ke Fk zadan behesh ro save mikone. 
    feature=models.ManyToManyField("Feature", through="ProductFeature")           # refer 1. ProductFeature esme table jadid hast
    
    def __str__(self):
            return f"{self.product_name}-{self.summary_description}"
    
    def get_absolute_url(self):
        return reverse("products:ProductDetail", kwargs={"slug": self.slug})                  # reverse be yek url ba in data ersal mikone. negah kon urls.py
    
    # #ref5 orders View. emale discounte DiscountBasket. discount 1/2 
    def get_price_by_discount(self):                                                          
        list1=[]
        for dbd in self.product_discountDetails.all():                                        # ref to discount => models. chon list hast all()
                if (dbd.discount_basket.is_active==True                                       # ba if() mitunim multi line benevism
                    and dbd.discount_basket.start_date <= datetime.now()
                    and datetime.now()<= dbd.discount_basket.end_date):
                    list1.append(dbd.discount_basket.discount)     
        discount=0
        if len(list1)>0:                                    # momkene yek product toye chand discountBasket bashe. pas max discount to mikhaym
            discount=max(list1)                             # discount 1/2
        return self.price-(self.price*discount/100)
    
    # tedade baghimonde az in product dar warehouse
    def get_number_in_warehouse(self):                      # ref to template => partials => products => type= 1
        sum1=self.product_warehouses.filter(warehouse_type_id=1).aggregate(Sum('qty'))           # aggregate means Sum. warehouse_type_id=1 means buy
        sum2=self.product_warehouses.filter(warehouse_type_id=2).aggregate(Sum('qty'))           # warehouse_type_id=1 mean selle
        
        input=0
        if sum1['qty__sum']!=None:                          # sum1 yek dict mishe ke yek key dare= 'qty__sum'
            input=sum1['qty__sum']
        
        output=0
        if sum2['qty__sum']!=None:
            output=sum2['qty__sum']
            
        return input-output
            
    # ref to app.comment_scoring_favorites.models => Scoring
    def get_average_score(self):
        avgScore=self.product_scores.all().aggregate(Avg('score'))['score__avg']         # mirize to dict ba key='score__avg'
        if avgScore == None:
            avgScore=0
        return avgScore
    
    
    # baraye peyda kardane usere jari(request.user) dakhele model az ravesh bayad raft. ref to middlewas dir => middlewares file
    def get_user_score(self):
        request=RequestMiddleware(get_response=None)
        request=request.thread_local.current_request
        user_score=self.product_scores.filter(scoring_user=request.user)
        
        score=0
        if user_score.count()>0:
            score=user_score[0].score               # chon filter yek list bar migardune
        return score
        
    # ref to apps.comment_scoring_favorites.models => Favorite
    def get_user_favorite(self):
        request=RequestMiddleware(get_response=None)
        request=request.thread_local.current_request
        flag=self.product_favorites.filter(favorite_user=request.user).exists()     # vaghti exists() mizarim tahesh => False ya True miyare
        return flag
    
    def getMainProductGroup(self):
        return self.product_group.all()[0].id                                   # avalin grohe in product ro miyare

    
    class Meta:
        verbose_name="Product Name"
        verbose_name_plural="Products Name"
        
#------------------------------------------------------------
class FeatureValue(models.Model):
    value_title=models.CharField(max_length=100)
    feature=models.ForeignKey("Feature", blank=True, null=True, on_delete=models.CASCADE, related_name="feature_values")      

    def __str__(self):
        return f"{self.id} {self.value_title}"
    
    class Meta:
        verbose_name="Value"
        verbose_name_plural="Values"


#------------------------------------------------------------
# look at the Admin => productName => end of the page => PRODUCTS FEATURES
class ProductFeature(models.Model):                                             # refer1, chon mikhaym default productFeature bridge table nadashte bashim, in model(bridge table) va refer 1 ro misazim.
    Product=models.ForeignKey("Product",on_delete=models.CASCADE, verbose_name="Product_Id", related_name="product_features")    # product one can have many ProductFeature. One product, many ProductFeature
    feature=models.ForeignKey("Feature",on_delete=models.CASCADE,verbose_name="feature_id")           # Feature one(model) can have many ProductFeature. one feature(Feature model) , many ProductFeature.
    value=models.CharField(max_length=100)                                        
    filter_value=models.ForeignKey("FeatureValue", on_delete=models.CASCADE, blank=True, null=True, related_name="features_of_value")    # why we use ForignKey => because it allows us to insert all of the other table into the fist table. Because it's Foriegn key, shows it as a dropdown in Admin page
    
    def __str__(self):
            return f"{self.Product} - {self.feature}: {self.value}"
    
    class Meta:
        verbose_name="Product Feature"
        verbose_name_plural="Products Features"

#------------------------------------------------------------
class ProductGallery(models.Model):
    product=models.ForeignKey("Product",on_delete=models.CASCADE,related_name="gallery_images")
    file_upload=FileUpload("images","product_gallery")
    image_name=models.ImageField(upload_to=file_upload.upload_to)
    
    class Meta:
        verbose_name= "Photo"
        verbose_name_plural="Photos"
        
#------------------------------------------------------------
# estefade az signals baraye delete image az server bad az delete yek record
# az 2 rahe zire mishe anjam dad vali behtare dar yek module jadid be esme signals.py benevisim. products.py => signals.py

# # rahe 1
# def delete_product_image(sender,**kwargs):              # bayad hatman in 2 vorodi ro dashte bashe
#     print(100*"*")
#     print("Product deleted1...")
#     print(100*"*")
    
# post_delete.connect(receiver=delete_product_image, sender=Product)

# #rehe 2
# @receiver(post_delete, sender=Product)
# def delete_product_image(sender,**kwargs):
#     print(100*"*")
#     print("Product deleted2...")
#     print(100*"*")