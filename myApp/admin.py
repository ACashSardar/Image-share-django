from django.contrib import admin
from .models import Image,Profile
# Register your models here.

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display=['id','photo','user','date']
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['id','user','email','about']