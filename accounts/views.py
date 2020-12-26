from django.shortcuts import render,redirect
import random
from Core.models import User
from django.contrib.auth.decorators import login_required
import string
from django.contrib import  messages
from listings.models import Listing
from django.contrib.auth import login,authenticate,logout
from django.core.mail import send_mail
from inquiry.models import inquiry
# Create your views here.
def randomString(stringlength=6):
    letter=string.ascii_letters
    return ''.join(random.choice(letter) for i in range(stringlength))

code=randomString()
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        password2 = request.POST['password2']
        user = User

        context ={
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'username': username,
            'phone': phone,
            'password': password,
        }

        if password == password2:
            if user.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('register')
            else:
                if user.objects.filter(email=email).exists():
                    messages.error(request, 'Email is already used')
                    return redirect('register')
                else:
                    if user.objects.filter(phone=phone).exists():
                        messages.error(request, 'Phone no  is already used')
                        return redirect('register')
                    else:
                        send_mail(
                            'Account Creation Confirmation',
                            'Hi '+ first_name + 'You Confirmation code is: ' +code,
                            'jaymangukiya0001@gmail.com',
                            [email],
                            fail_silently=False
                        )
                        request.method = 'GET'
                        return render(request, 'accounts/confirmregister.html', context)
        else:
            messages.error(request,'passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def confirmregister(request):
    if request.method=='POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirmcode = request.POST['confirmcode']
        user = User

        context ={
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'username': username,
            'phone': phone,
            'password': password,
        }

        if code==confirmcode:
            user=user.objects.create_user(username=username,password=password,email=email,phone=phone,first_name=first_name,last_name=last_name)
            user.save()
            login(request,user)
            messages.success(request,"you are now logged in")
            return redirect('index')
        else:
            messages.error(request,'Invalid confirmation code')
            return render(request,'accounts/confirmregister.html',context)
    else:
        return redirect('register')



def userLogin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You are now logged in")
            return redirect('index')
        else:
            messages.error(request,'Invalid constrains')
            return redirect('login')
    else:
        return render(request,'accounts/login.html')


@login_required
def userLogout(reuqest):
    if reuqest.method=='POST':
        logout(reuqest)
        messages.success(reuqest,"You are now logged out")
        return redirect('index')


@login_required
def dashboard(request):
    mylisting=Listing.objects.order_by('-last_date').filter(owner=request.user)
    context={
        'listings':mylisting,
    }
    return render(request,'accounts/dashboard.html',context)

@login_required
def myinquiries(request):
    myinquiry=inquiry.objects.all().filter(user_id=request.user.id)
    
    context={
        'myinquiries':myinquiry,
    }
    return render(request,'accounts/dashboard_myinquiries.html',context)

@login_required
def inquiry1(request):
    myinquiry=inquiry.objects.all().filter(owner_id=request.user.id)
    print('inn')
    print(myinquiry)
    context={
        'inquiries':myinquiry,
    }
    return render(request,'accounts/dashboard_inquiries.html',context)


@login_required
def send_reply(request):
    if request.method =="POST":
        email = request.POST['email']
        message = request.POST['message']
        lisiting = request.POST['listing']
        send_mail(
            'Reply from ' + lisiting + ' owner',
            message,
            'jaymangukiya0001@gmail.com',
            [email],
            fail_silently=False
        )
        messages.success(request, 'Your reply has been sent successfully')
        return redirect('inquiry1')
    else:
        return redirect('dashboard')