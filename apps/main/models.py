from django.db import models
from utils import FileUpload
from django.utils import timezone
from django.utils.html import mark_safe
from apps.products.models import Product

class Slider(models.Model):
    slider_title1=models.CharField(max_length=500, blank=True, null=True, verbose_name="slider1")
    slider_title2=models.CharField(max_length=500, blank=True, null=True, verbose_name="slider2")
    slider_title3=models.CharField(max_length=500, blank=True, null=True, verbose_name="slider3")
    file_upload=FileUpload('images','slides')
    image_name=models.ImageField(upload_to=file_upload.upload_to)
    slider_link=models.URLField(max_length=200, null=True,blank=True)       # URLField
    is_active=models.BooleanField(default=True, blank=True)
    register_date=models.DateTimeField(auto_now_add=True)
    published_date=models.DateTimeField(default=timezone.now)
    update_date=models.DateTimeField(auto_now=True)
    product= models.OneToOneField(Product, on_delete = models.CASCADE,blank=True, null=True, related_name="slider")
    
    
    def __str__(self):
        return f"{self.slider_title1}"
    
    class Meta:
        verbose_name="Slide"
        verbose_name_plural="Slides"
        
    def image_slide(self):                                              # bejaye dade in html ro mifreste. dar admin.py in html ro neshun dadim
        return mark_safe(f'<img src="/media/{self.image_name}" style="width:80px; height:80px;"/>')
    image_slide.short_description= "slide image"
    
    def link(self):                                                    # be admin.py in html ro mifreste
        return mark_safe(f"<a href='{self.slider_link}' target='_blank'>link</a>")
    link.short_description="links"