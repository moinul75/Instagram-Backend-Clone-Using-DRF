from django.db import models
from App.manage import UserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = None 
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100,unique=True)
    bio = models.CharField(max_length=255,blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    
#post model 
class Post(models.Model):
    title = models.CharField(max_length=255)
    descriptions = models.CharField(max_length=520)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    

#like model 
class PostLike(models.Model):
    user = models.ForeignKey(User,null=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,null=False, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (("user","post"),)
    
#Comment model 
class CommentPost(models.Model):
    comment_text = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,null=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=False)
    

#follow model 
class FollowUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False, related_name='src_user')
    follows = models.ForeignKey(User,on_delete=models.CASCADE,null=False, related_name='dest_user')
    


     
    
    
    
