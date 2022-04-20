from django.shortcuts import redirect, render
from .models import Image,Profile, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as UserLogin, logout as UserLogout
from nltk.stem.porter import PorterStemmer

# Create your views here.
ps=PorterStemmer()
def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))

    return " ".join(y)

def home(request): 
    if request.method=="POST":
        photo=request.FILES['photo']
        checkbox=None
        try:
            checkbox=request.POST['chbx']
        except:
            print('checkbox=',checkbox)
        newcatg=request.POST['newcatg']
        category=Category.objects.get(title=request.POST['category'])
        if photo:
            if checkbox and newcatg:
                category=Category.objects.create(title=newcatg)
                photo=Image.objects.create(photo=photo, user=request.user, catg=category)
            else:
                photo=Image.objects.create(photo=photo, user=request.user, catg=category)

    images=Image.objects.all()
    if request.user.is_authenticated and request.method=="POST":
        images=Image.objects.filter(user=request.user)
        userinfo=Profile.objects.filter(user=request.user)
        category=Category.objects.all()
        print('Available categories',category)
        context={'images':images,'userinfo':userinfo,'category':category,'visitor':False}
        return render(request,'dashboard.html',context)
    elif request.user.is_authenticated and request.method=="GET":
        images=Image.objects.all()
        userinfo=Profile.objects.filter(user=request.user)
        category=Category.objects.all()
        context={'images':images,'userinfo':userinfo,'category':category,'visitor':False,'registered':True}
        return render(request,'homepage.html',context)
    else:
        category=Category.objects.all()
        context={'images':images,'category':category,'visitor':False,'registered':False}
        return render(request,'homepage.html',context)       

def dashboard(request):
    category=Category.objects.all()
    images=Image.objects.filter(user=request.user)
    userinfo=Profile.objects.filter(user=request.user)
    context={'images':images,'userinfo':userinfo,'category':category,'visitor':False}
    return render(request,'dashboard.html',context)

def editprofile(request):
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
    category=Category.objects.all()
    context={'images':images,'userinfo':userinfo,'category':category}
    return render(request,'editprofile.html',context)

def delete(request,imageID,curr_page):
    try:
        item=Image.objects.get(pk=imageID)
        item.photo.delete()
        item.delete()
    except:
        pass
    category=Category.objects.all()
    images=Image.objects.filter(user=request.user)
    userinfo=Profile.objects.filter(user=request.user)
    context={'images':images,'userinfo':userinfo, 'category':category,'registered':True}
    if curr_page=='homepage':
        images=Image.objects.all()
        context={'images':images,'userinfo':userinfo, 'category':category,'registered':True}
        return render(request,'homepage.html',context)
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
            return redirect('login')
        else:
            return render(request,"signup.html",context)
    return render(request,"signup.html",context)

def logout(request):
    UserLogout(request)
    print('logged out')
    return redirect('signup')

def onclick(request,username):
    allprof=Profile.objects.all()
    for ap in allprof:
        print(ap.user," ",username)
        if str(ap.user)==username:
            images=Image.objects.filter(user=ap.user)
            category=Category.objects.all()
            userinfo=Profile.objects.filter(user=ap.user)
    context={'images':images,'userinfo':userinfo,'category':category,'visitor':True}
    return render(request,'dashboard.html',context)

def catgsearch(request,catg):
    allcatg=Category.objects.all()
    images=Image.objects.all()
    category=Category.objects.all()
    if catg=="allimg":
        images=Image.objects.all()
    else:
        for ac in allcatg:
            if str(ac.title)==catg:
                images=Image.objects.filter(catg=ac)
    context={'images':images,'category':category,'visitor':False,'registered':request.user.is_authenticated}
    return render(request,'homepage.html',context)
    
def manualsearch(request):
    userSearch=request.POST['searchbar']
    userSearch=stem(userSearch)
    userSearch = list(userSearch.split(" "))
    allcatg=Category.objects.all()
    images=Image.objects.none()
    for ac in allcatg:
        for word in userSearch:
            if word in stem(str(ac.title)):
                images=Image.objects.filter(catg=ac)
    category=Category.objects.all()
    context={'images':images,'category':category,'visitor':False,'registered':request.user.is_authenticated}
    return render(request,'homepage.html',context)


def selectimg(request,catg,id):
    print(catg,id)
    images=Image.objects.none()
    category=Category.objects.get(title=catg)
    images=Image.objects.filter(catg=category)
    selectedimg=images.get(id=id)
    images=images.exclude(id=id)
    profile=Profile.objects.get(user=selectedimg.user)
    visitor=True
    registered=False
    if request.user.is_authenticated:
        registered=True
    if str(request.user)==str(selectedimg.user):
        visitor=False
        registered=True
    select=True
    category=Category.objects.all()
    context={'images':images,'category':category,'visitor':visitor,'selectedimg':selectedimg,'select':select,'profile':profile,'registered':registered}
    select=False
    return render(request,'homepage.html',context)
