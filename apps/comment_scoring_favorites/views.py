from django.shortcuts import render,get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.http import HttpResponse
from .forms import CommentForm
from apps.products.models import Product
from .models import Comment, Scoring, Favorite
from django.db.models import Q

#------------------------------------------------------------------
class CommentView(View):
    # 1. age be sorate data az API biyad dar get(url) neshun dade nemishe va bayad az tarighe request.GET.get() begirimesh
    # 2. age be sorate params(querystring) biyad dar get(url) neshun dade mishe. be sorate params => bayad to urls.py(API) benevisim masaln /slug:slug/
    
    def get(self, request, *args, **kwargs):
        # first comment these two below lines are None
        productId=request.GET.get('productId')              # be sorate data omade
        commentId=request.GET.get('commentId')
        slug=kwargs['slug']                                 # be sorate params omade
        initial_dict={
            "product_id":productId,
            "comment_id":commentId
        }
        form= CommentForm(initial= initial_dict)            # ba in dataha por kon. faghat bayad fieldhaye product_id va comment_id bashe to form
        return render(request,'csf_app/partials/create_comment.html',{"form":form,"slug":slug})             # in return dakhele res ferestade mishe be ajax
        
        
    def post(self,request,**kwargs):
        slug=kwargs.get('slug')          # kwargs['slug]
        form=CommentForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            product=get_object_or_404(Product, slug=slug)
            
            parent=None
            if (cd['comment_id']):                              # First comment, comment_id is None
                parent_comment_id=cd['comment_id']
                parent=Comment.objects.get(id=parent_comment_id)
                
            Comment.objects.create(
                product=product,
                commenting_user=request.user,
                comment_text=cd['comment_text'],
                comment_parent=parent,
            )
                
            messages.success(request,"your comment is sent","success")
            return redirect("products:ProductDetail",product.slug)
        messages.error(request,"error in sending comment","danger")
        return redirect("products:ProductDetail",product.slug)
       
#------------------------------------------------------------------    
def add_score(request):
       productId=request.GET.get("productId")
       score=request.GET.get("score")
       
       product=Product.objects.get(id=productId)
       Scoring.objects.create(
           product=product,
           scoring_user=request.user,
           score=score
       )
       
       return HttpResponse("your Score is added")
   

def add_to_favorite(request):
    productId=request.GET.get('productId')
    product=Product.objects.get(id=productId)
    
    flag=Favorite.objects.filter(Q(product=productId) & Q(favorite_user=request.user.id)).exists()              # exists true ya False bar migardune
    if (not flag):
        Favorite.objects.create(
            product=product,
            favorite_user=request.user
        )
        return HttpResponse("this product is added to your Favorite")
    return HttpResponse("this product already added to your Favorite")

def remove_from_favorite(request):
    productId=request.GET.get("productId")    
    
    flag=Favorite.objects.filter(Q(product=productId) & Q(favorite_user=request.user.id)).exists()

    if (not flag):
        return HttpResponse("This product is not in your favorite list")
    favoriteObj = Favorite.objects.get(Q(product_id = productId) & Q(favorite_user = request.user.id))
    favoriteObj.delete()
    return HttpResponse("This product removed from your favorite list")    
    
    
    
    # product=Product.objects.get(id=productId)

    
    # if product:
    #     # flag = Favorite.objects.filter(Q(product=productId) & Q(favorite_user=request.user.id)).exists()
    #     product.delete()
    #     # if (not flag):
    #     #     Favorite.objects.delete(int(productId))
class UserFavoriteView(View):
    def get(self, request, *args, **kwargs):
        user_favorite=Favorite.objects.filter(Q(favorite_user=request.user.id))
        return render(request,'csf_app/user_favorite.html',{'user_favorite':user_favorite})