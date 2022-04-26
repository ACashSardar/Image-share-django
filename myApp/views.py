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

def showFeeds(user):
    curr_user=Profile.objects.get(user=user)
    feeds=Image.objects.none()
    for i in range(curr_user.followings.all().count()):
        if i==0 and user.is_superuser:
            continue
        feeds= feeds | Image.objects.filter(user=curr_user.followings.all()[i])
    return feeds

def home(request): 
    if request.method=="POST":
        checkbox=None
        photo=None
        capt=request.POST['caption']
        try:
            photo=request.FILES['photo']
            checkbox=request.POST['chbx']
        except:
            print('checkbox=',checkbox)
        newcatg=request.POST['newcatg']
        category=Category.objects.get(title=request.POST['category'])
        if photo:
            if checkbox and newcatg:
                category=Category.objects.create(title=newcatg)
                photo=Image.objects.create(photo=photo, user=request.user,capt=capt, catg=category)
            else:
                photo=Image.objects.create(photo=photo, user=request.user,capt=capt, catg=category)

    images=Image.objects.all()
    if request.user.is_authenticated and request.method=="POST":
        images=Image.objects.filter(user=request.user)
        userinfo=Profile.objects.filter(user=request.user)
        category=Category.objects.all()
        feeds=showFeeds(request.user)
        context={'images':images,'userinfo':userinfo,'category':category,'visitor':False, 'feeds': feeds}
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
    feeds=showFeeds(request.user)
    context={'images':images,'userinfo':userinfo,'category':category,'visitor':False, 'feeds': feeds}
    return render(request,'dashboard.html',context)

def editprofile(request):
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
    feeds=showFeeds(request.user)
    context={'images':images,'userinfo':userinfo,'visitor':False, 'feeds': feeds}
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
    feeds=showFeeds(request.user)
    context={'images':images,'userinfo':userinfo, 'category':category,'registered':True, 'feeds': feeds}
    if curr_page=='homepage':
        images=Image.objects.all()
        context={'images':images,'userinfo':userinfo, 'category':category,'registered':True, 'feeds': feeds}
        return render(request,'homepage.html',context)
    return render(request,'dashboard.html',context)

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        print('User logged In')
        if user:
            profile=Profile.objects.all()
            present=False
            for pr in profile:
                if(str(pr.user)==username):
                    present=True
                    break
            if(present is False):
                profile=Profile.objects.create(user=user)
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
    member=False
    follow=False
    visitor=True
    targetuser=None
    followedBy=None
    for ap in allprof:
        if str(ap.user)==username:
            images=Image.objects.filter(user=ap.user)
            category=Category.objects.all()
            userinfo=Profile.objects.filter(user=ap.user)
            targetuser=ap
            break
    for ap in allprof:
        if str(ap.user)==str(request.user):
            followedBy=ap
            break
    if request.user.is_authenticated:
        member=True
    if str(targetuser.user)==str(request.user):
        visitor=False
    if member and targetuser.user in followedBy.followings.all():
        follow=True
    context={'images':images,'userinfo':userinfo,'category':category,'visitor':visitor,'follow':follow, 'member':member}
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

def follow(request,profileID):
    profile=Profile.objects.get(id=profileID)
    follow=False
    allprof=Profile.objects.all()
    for ap in allprof:
        if str(ap.user)==str(request.user):
            followedBy=ap
            break

    if profile.user in followedBy.followings.all():
        profile.followers.remove(followedBy.user)
        followedBy.followings.remove(profile.user)
        follow=False
        print('Unfollowed')
    
    else:
        profile.followers.add(followedBy.user)
        followedBy.followings.add(profile.user)
        follow=True
        print('Followed')
    images=Image.objects.filter(user=profile.user)
    category=Category.objects.all()
    userinfo=Profile.objects.filter(user=profile.user)
    context={'images':images,'userinfo':userinfo,'category':category,'visitor':True, 'follow':follow,'member':True}
    return render(request,'dashboard.html',context)
    