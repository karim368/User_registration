from django.shortcuts import render

# Create your views here.
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def registration(request):
    euf = UserForm()
    epf = ProfileForm()
    d = {'euf':euf,'epf':epf}
    if request.method == 'POST' and request.FILES:
        ufdo = UserForm(request.POST)
        pfdo = ProfileForm(request.POST,request.FILES)
        if ufdo.is_valid() and pfdo.is_valid():
            mufdo = ufdo.save(commit=False)
            pw = ufdo.cleaned_data['password']
            mufdo.set_password(pw)
            mufdo.save()

            mpfdo = pfdo.save(commit=False)
            mpfdo.username = mufdo
            mpfdo.save()

            send_mail(
                'Registration',
                'Thanks for Registering to my DataBase',
                'karimphatan9@gmail.com',
                [mufdo.email],
                fail_silently = False,
            )
            return HttpResponse('Registration is successfull')
        else:
            return HttpResponse('Invalid Data')
        
    return render(request,'registration.html',d)

def home(request):
    if request.session.get('username'):
        username = request.session.get('username')
        d = {'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['un']
        password = request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username'] = username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid Credentials')
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def profile_display(request):
    un = request.session.get('username')
    UO = User.objects.get(username=un)
    PO = Profile.objects.get(username=UO)
    d = {'UO':UO,'PO':PO}
    return render(request,'profile_display.html',d)

@login_required
def change_password(request):
    if request.method == 'POST':
        password = request.POST['pw']
        username = request.session.get('username')
        UO = User.objects.get(username=username)
        UO.set_password(password)
        UO.save()
        return HttpResponse('Password Chaged successfully')
    return render(request,'change_password.html')

def reset_password(request):
    if request.method == 'POST':
        username = request.POST['un']
        password = request.POST['pw']
        LUO = User.objects.filter(username=username)
        if LUO:
            UO = LUO[0]
            UO.set_password(password)
            UO.save()
            return HttpResponse('Reset of password is done successfully')
        else:
            return HttpResponse('Your username is not in our DataBase')
    return render(request,'reset_password.html')
# nisz vlsz lgvk tkpi