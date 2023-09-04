from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.http import HttpResponse
from .models import Record
from django.template import loader
from django.urls import reverse
# Create your views here.
def home(request):
    records=Record.objects.all()
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"SUCCESFULLY LOGGEDIN")
            return redirect('home')
        else:
            messages.success(request,"There was error in logging in ,please try again")
            return redirect('home')
    else:
        return render(request,'home.html',{'records':records})

def logout_user(request):
    logout(request)
    messages.success(request,"You have been succesfully logged out...")
    return redirect('home')
def register(request):
    if request.method=='POST':
        username=request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        password1=request.POST['password1']
        password2=request.POST['password2']
        email=request.POST['email']
        if(password1==password2):
            if User.objects.filter(username=username).exists():
                messages.info(request,"username taken")
                return redirect('register/')

            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email Taken")
                return redirect('register/')

            else:
                user=User.objects.create_user(username=username,password=password1,email=email,first_name=firstname,last_name=lastname)

                login(request,user)
                user.save()
                messages.info(request,"Registration successful")
                return redirect('/')

        else:
            messages.info(request,"Password Not matching")
            return redirect('register/')
    else:
        return render(request,'register.html',{})

def customer_record(request,pk):
    if request.user.is_authenticated:
        customer_record=Record.objects.get(id=pk)
        return render(request,'record.html',{'customer_record':customer_record})
    else:
        messages.success(request,"You must login to view that page")
        return redirect('home')


def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_it=Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,"You have beem Successfully deleted")
        return redirect('home')
    else:
        messages.success(request,"You must need to login to delete this details")
        return redirect('home')

def add_record(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            firstname=request.POST['first_name']
            lastname=request.POST['last_name']
            email=request.POST['email']
            phone=request.POST['phone']
            address=request.POST['address']
            city=request.POST['city']
            state=request.POST['state']
            zipcode=request.POST['Zipcode']
            user=Record.objects.create(first_name=firstname,phone=phone,email=email,address=address,last_name=lastname,city=city,state=state,Zipcode=zipcode)
            user.save()
            messages.success(request,"Record added Successful")
            return redirect('home')
        else:
             return render(request,'add.html',{})
    else:
        messages.success(request,"You need to login to add data")
        return redirect('home')
  
def update_record(request,pk):
        if request.user.is_authenticated:
            current_record=Record.objects.get(id=pk)
            template=loader.get_template('update.html')
            context={
                'current_record':current_record,
            }
            return HttpResponse(template.render(context,request))

def updaterecord(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            firstname=request.POST['first_name']
            lastname=request.POST['last_name']
            email=request.POST['email']
            phone=request.POST['phone']
            address=request.POST['address']
            city=request.POST['city']
            state=request.POST['state']
            zipcode=request.POST['Zipcode']
            user=Record.objects.get(id=id)
            user.first_name=firstname
            user.last_name=lastname
            user.email=email
            user.phone=phone
            user.address=address
            user.city=city
            user.state=state
            user.Zipcode=zipcode

            user.save()
            messages.success(request,"Record updated Successful")
            return redirect('home')
           
        else:
             
            current_record = Record.objects.get(id=id)
            return render(request,'update.html',{'current_record':current_record})
    else:
        messages.success(request,"You need to login to add data")
        return redirect('home')
    
