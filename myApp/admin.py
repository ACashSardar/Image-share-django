from django.contrib import admin
from .models import Image,Profile, Category
# Register your models here.

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display=['id','photo','user','capt','catg','date']
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['id','user','email','about']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','title']