from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, LoginForm
from .models import Post
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

def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def index(request):
    try:
        name = request.user.name
        if name:
            return render(request, 'index.html', {'name':name})
    except:
        return render(request, 'index.html', {'name':'GUEST'})


def board_create(request):
    # 로그인 예외 처리
    if not request.user.is_authenticated:
        messages.error(request, '페이지에 접근할 권한이 없습니다.')
        return redirect('index')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Post.objects.create(author=request.user, title=title, content=content)
        return redirect('board_list')
    return render(request, 'board_create.html')


def board_edit(request, pk):
    # 로그인 예외 처리
    if not request.user.is_authenticated:
        messages.error(request, '페이지에 접근할 권한이 없습니다.')
        return redirect('index')
    
    # post 객체 존재 여부에 대한 예외 처리
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        messages.error(request, "잘못된 접근입니다.")
        return redirect('board_list')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post.title = title
        post.content = content
        # 게시글 수정 권한 여부 확인
        if post.author == request.user or post.author.is_staff == 1:
            post.save()
        else:
            messages.error(request, '권한이 없습니다.')
            return redirect('board_list')
        return redirect('board_detail', pk=pk)
    return render(request, 'board_edit.html', {'post':post})


def board_delete(request, pk):
    # 로그인 예외 처리
    if not request.user.is_authenticated:
        messages.error(request, '페이지에 접근할 권한이 없습니다.')
        return redirect('index')
    
    # post 객체 존재 여부에 대한 예외 처리
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        messages.error(request, "잘못된 접근입니다.")
        return redirect('board_list')
    
    # 게시글 삭제 권한 여부 확인
    if post.author == request.user or post.author.is_staff == 1:
        post.delete()
    else:
        messages.error(request, '권한이 없습니다.')
    return redirect('board_list')


def board_list(request):
    # 로그인 예외 처리
    if not request.user.is_authenticated:
        messages.error(request, '페이지에 접근할 권한이 없습니다.')
        return redirect('index')
    posts = Post.objects.all().order_by('-pk') # pk 내림차순
    return render(request, 'board_list.html', {'posts':posts})


def board_detail(request, pk):
    # 로그인 예외 처리
    if not request.user.is_authenticated:
        messages.error(request, '페이지에 접근할 권한이 없습니다.')
        return redirect('index')
    
    # post 객체 존재 여부에 대한 예외 처리
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        messages.error(request, "해당 포스트가 존재하지 않습니다.")
        return redirect('board_list')
    return render(request, 'board_detail.html', {'post':post})