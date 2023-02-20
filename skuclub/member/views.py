from django.shortcuts import render, redirect
from .models import Account
from .forms import SignUpForm, LoginForm

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
        form = LoginForm(request.POST)
        if form.is_valid():
            user_email = Account.objects.filter(
                account_email = form.cleaned_data['account_email'],
                account_pw = form.cleaned_data['account_pw']
            )
            if not user_email:
                return render(request, 'login.html', {'form':form, 'login_fail':True})
            request.session['user_id'] = form.cleaned_data['account_email']
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form, 'login_fail':False})

def index(request):
    email = request.session.get('user_id')
    if email:
        name = Account.objects.get(account_email=email)
        if name:
            return render(request, 'index.html', {'name':name.account_name})
    return render(request, 'index.html', {'name':'GUEST'})
