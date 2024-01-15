from django.db import models
from apps.products.models import Product
from apps.accounts.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator

#--------------------------------------------------------------------------
class Comment(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE, related_name="product_comments")
    commenting_user=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_comments", verbose_name="user who comment")
    approving_user=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_approvedComments2", verbose_name="user approved comment", null=True, blank=True)         # useri k comment ro tayid karde
    comment_text=models.TextField()
    registerdate=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)            # we can put the default=False, because first admin needs to approve it in admin page then show 
    comment_parent=models.ForeignKey("Comment", on_delete=models.CASCADE,null=True, blank=True, related_name="child_comments")                # self join. null va blank bayad True bashe chon momkene avalin comment bashe
    
    def __str__(self):
        return f"{self.product} - {self.commenting_user}"
    
    class Meta:
        verbose_name="comment"
        verbose_name_plural="comments"

#--------------------------------------------------------------------------
class Scoring(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE, related_name="product_scores")
    scoring_user=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_scores")
    registerDate=models.DateTimeField(auto_now_add=True)
    score=models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    
    def __str__(self):
        return f"{self.product} - {self.scoring_user}"

    class Meta:
        verbose_name="score"
        verbose_name_plural="scores"
        
#--------------------------------------------------------------------------
class Favorite(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_favorites")
    favorite_user=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_favorites")
    register_date=models.DateTimeField(auto_now_add= True)
    
    def __str__(self):
        return f"{self.product} - {self.favorite_user}"
    
    class Meta:
        verbose_name="favorite"
        verbose_name_plural="favorites"
