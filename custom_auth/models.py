from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password,full_name,phone_number, **extra_fields):
        print(password,'jjjjjjjjjjjjj')
        if not email:
            raise ValueError(_('Users must have an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email,full_name=full_name,phone_number=phone_number)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user
   
class User(AbstractUser):
    email           = models.EmailField(_('email address'), unique=True)
    name            = models.CharField(max_length=35,null=True)
    phone_number    = models.CharField(max_length=35,null=True)
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    username = None  # Set username to None to prevent its creation

    def __str__(self):
        return self.email

class PostBlog(models.Model):
    user            = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    place_name      = models.CharField(max_length = 50)
    image           = models.ImageField(upload_to='images/')
    discription     = models.TextField()
    start_date      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.place_name
    
    def save(self, *args, **kwargs):
        if not self.pk:  
            self.start_date = timezone.now()
        return super().save(*args, **kwargs)

class CommentOnBlog(models.Model):
    user            = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    blog            = models.ForeignKey(PostBlog,on_delete=models.CASCADE,null=True)
    message         = models.TextField()
    start_date      = models.DateTimeField(auto_now_add=True,null=True)
    def save(self, *args, **kwargs):
        if not self.pk:  
            self.start_date = timezone.now()
        return super().save(*args, **kwargs)

    
    def __str__(self):
        return self.id
    
class LikeOnBlog(models.Model):
    user            = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    blog         = models.ForeignKey(PostBlog,on_delete=models.CASCADE,null=True)
    start_date      = models.DateTimeField(auto_now_add=True,null=True)
    

    def __str__(self):
        return self.id
    def save(self, *args, **kwargs):
        if not self.pk:  
            self.start_date = timezone.now()
        return super().save(*args, **kwargs)



    



