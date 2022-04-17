import email
from django.db import models
from django.forms import DateTimeField, FileField
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    email=models.EmailField(blank=True, null=True)
    about=models.TextField(blank=True, null=True)
    def __str__(self):
        return str(self.user) 

class Category(models.Model):
    title=models.CharField(max_length=100)
    def __str__(self):
        return self.title  

class Image(models.Model):
    photo=models.ImageField(upload_to="allimages")
    date=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    catg=models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)
