from django.shortcuts import redirect, render
from matplotlib.pyplot import title
from .models import Image,Profile, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as UserLogin, logout as UserLogout

# Create your views here.

def home(request): 
    if request.method=="POST":
        photo=request.FILES['photo']
        category=Category.objects.get(title=request.POST['category'])
        if photo and category:
            photo=Image.objects.create(photo=photo, user=request.user, catg=category)

    images=Image.objects.all()
    if request.user.is_authenticated:
        images=Image.objects.filter(user=request.user)
        userinfo=Profile.objects.filter(user=request.user)
        category=Category.objects.all()
        print(category)
        context={'images':images,'userinfo':userinfo,'category':category,'visitor':False}
        return render(request,'dashboard.html',context)
    else:
        category=Category.objects.all()
        context={'images':images,'category':category}
        return render(request,'homepage.html',context)       

def dashboard(request):
    category=Category.objects.all()
    images=Image.objects.filter(user=request.user)
    userinfo=Profile.objects.filter(user=request.user)
    context={'images':images,'userinfo':userinfo,'category':category,'visitor':False}
    return render(request,'dashboard.html',context)

def editprofile(request):
    print('request.user.id',request.user.id)
    profile=Profile.objects.all()
    present=False
    for pr in profile:
        if(str(pr.user)==str(request.user)):
            present=True
            break
    if(present is False):
        profile=Profile.objects.create(user=request.user)

    if request.method=='POST':
        email=request.POST['email']
        about=request.POST['about']
        userinfo=Profile.objects.get(user=request.user)
        userinfo.email=email
        userinfo.about=about
        userinfo.save()
        redirect('dashboard')
    images=Image.objects.filter(user=request.user)
    userinfo=Profile.objects.get(user=request.user)
    context={'images':images,'userinfo':userinfo}
    return render(request,'editprofile.html',context)

def delete(request,imageID):
    try:
        item=Image.objects.get(pk=imageID)
        item.photo.delete()
        item.delete()
    except:
        pass
    category=Category.objects.all()
    images=Image.objects.filter(user=request.user)
    userinfo=Profile.objects.filter(user=request.user)
    context={'images':images,'userinfo':userinfo, 'category':category}
    return render(request,'dashboard.html',context)

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        print('User logged In')
        if user:
            UserLogin(request,user)
            return redirect('dashboard')
    return render(request,'login.html')

def signup(request): 
    form=UserCreationForm()
    context={'form':form}
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        context={'form':form}
        if form.is_valid():
            form.save()
            # Profile.objects.create(user=request.user,email='None@gmail.com')
            return redirect('login')
        else:
            return render(request,"signup.html",context)
    return render(request,"signup.html",context)

def logout(request):
    UserLogout(request)
    print('logged out')
    return redirect('signup')

def authuserhome(request):
    images=Image.objects.all()
    category=Category.objects.all()
    context={'images':images,'category':category}
    return render(request,'authuserhome.html',context)

def onclick(request,username):
    allprof=Profile.objects.all()
    print(allprof)
    for ap in allprof:
        print(ap.user," ",username)
        if str(ap.user)==username:
            images=Image.objects.filter(user=ap.user)
            category=Category.objects.all()
            userinfo=Profile.objects.filter(user=ap.user)
    context={'images':images,'userinfo':userinfo,'category':category,'visitor':True}
    return render(request,'dashboard.html',context)