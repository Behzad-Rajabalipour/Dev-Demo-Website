# bade delete yek record image un az server hazf nemishod baraye hamin signals estefade mikonim.
# model haye digeye signals dar site django models signals  
# aval bayad toye apps => products => apps.py
from django.dispatch import receiver
from django.db.models.signals import post_delete            # model haye digeye signals dar site django models signals  
from .models import Product
from django.conf import settings
import os

@receiver(post_delete, sender=Product)
def delete_product_image(sender,**kwargs):
    path=settings.MEDIA_ROOT+str(kwargs["instance"].image_name)          # kwargs["instance"] un recorde delete shode ro miyare. instance nemune delete shode hast
    if os.path.isfile(path):
        os.remove(path)                                                  # aks az sever pak mishe