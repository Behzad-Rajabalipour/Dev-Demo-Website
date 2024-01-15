from django.shortcuts import render
from apps.products.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from .Serializers import ProductSerializer
from CustomPermission import CustomPermissionForProducts

# bejaye in ke page baz kone khorojiye API(json) mide ke yek application dige mitune begirash

# 1. cmd => pip install djangorestframework
# 2. settings.py => INSTALLED_APPS => ezafe mikonim "rest_framework"
# 3. hala mitunim to moduleha az rest_framework estefade konim
class AllPoductsApi(APIView):
    permission_classes=[CustomPermissionForProducts]            # permission. esmesh hatman bayad permission_classes bashe
    def get(self, request):
        products=Product.objects.filter(is_active=True).order_by("-published_date")
        self.check_object_permissions(request,products)         # baraye products permission haye permission_classes ro check kon
        ser_data=ProductSerializer(instance=products, many=True)        # baraye API bayad serialize konim
        return Response(data=ser_data.data)