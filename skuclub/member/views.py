from django.shortcuts import render, redirect
from .models import Account
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from django.core.exceptions import ValidationError

def signup(request):
    email_error = False
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        if 'account_email' in form.errors:
            email_error = True
    else:
        form = SignUpForm()
        
    return render(request, 'signup.html', {'form':form, 'email_error':email_error})

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_email = Account.objects.filter(
            account_email = email,
            account_pw = password
        )
        if not user_email:
            return render(request, 'login.html', {'login_fail':True})
        return render(request, 'login.html', {'login_success':True, 'email':email})
    return render(request, 'login.html', {'login_fail':False})

def index(request):
    if 'email' in request.GET:
        name = Account.objects.get(account_email=request.GET['email']).account_name
        return render(request, 'index.html', {'name':name})
    return render(request, 'index.html', {'name':'GUEST'})
