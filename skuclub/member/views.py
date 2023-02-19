from django.shortcuts import render, redirect
from .models import Account

def signup(request):
    if request.method == 'POST':
        Account.objects.create(
            account_email = request.POST['email'],
            account_pw = request.POST['password'],
            account_name = request.POST['name'],
        )
        return redirect('login')
    return render(request, 'signup.html')

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
