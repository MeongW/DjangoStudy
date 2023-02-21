from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, LoginForm

def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form':form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error('password', "로그인에 실패하였습니다.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})

def index(request):
    try:
        name = request.user.name
        if name:
            return render(request, 'index.html', {'name':name})
    except:
        return render(request, 'index.html', {'name':'GUEST'})
