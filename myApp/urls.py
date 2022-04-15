from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('authuserhome/', views.authuserhome,name='authuserhome'),
    path('editprofile/', views.editprofile,name='editprofile'),
    path('login/', views.login,name='login'),
    path('signup/', views.signup,name='signup'),
    path('logout/', views.logout,name='logout'),
    path('delete/<int:imageID>', views.delete,name='delete'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)