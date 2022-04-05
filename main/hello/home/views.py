import email
import re
from django.shortcuts import get_object_or_404, render , HttpResponse , redirect , get_list_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from .models import postss ,messagess, reviews
from django.contrib.auth import authenticate , login,logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import os
def loginpage(request):
    page = 'login'
    if request.method =='POST':
        username= request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
          user = user.objects.get(username=username)
        except:
            messages.error(request , 'user does not exist')
        user = authenticate(request , username = username , password = password)
        if user is not None:
            login(request  , user)
            return redirect('home')    
    context = {'page': page}
    return render(request ,'login.html',context)
# Create your views here.
def logoutuser(request):
    logout(request)
    return redirect('login')

def registeruser(request):
    page = 'register'
    form =  UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username  = user.username.lower()
            user.save()
            login(request , user)
            return redirect('home')


    context = {'form':form}
    return render(request , 'login.html' , context)
@login_required(login_url='/login')
def index(request):
    item = postss.objects.all()
    context = { 'items':item}
    
    return render(request ,'index.html',context)
@login_required(login_url='/login')
def mes(request , pk):
    user = User.objects.get(id = pk)
    meso = messagess.objects.filter(recievers=user)
    if meso :
        m = 'yes'
    else:
        m='no'    
    context = {'messages':meso,'m':m}
    return render(request , 'blank.html' , context)

def userprofile(request,pk ):
     user = User.objects.get(id=pk)
     review = reviews.objects.get(person_reviewed=user)
     context = {'user':user,'reviews':review}

     return render(request , 'profile.html',context )    
def contact(request ):
    if request.method == "POST":
        print(request.user)
        nam = request.POST.get('name')
        passwor = request.POST.get('number')
        img = request.FILES['image']
        pr = postss(name = nam , number = passwor , image = img , host = request.user)
        pr.save()     

    return render(request , 'contact.html')

