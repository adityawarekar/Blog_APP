from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Posts

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  

    if request.method == 'POST':
        uname = request.POST.get('uname')
        upassword = request.POST.get('upassword')

        user = authenticate(username=uname, password=upassword)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'blog/login.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')  

    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        user = User.objects.create_user(
            username=email,
            first_name=fullname,
            email=email,
            password=password
        )
        user.save()
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'blog/signup.html')


def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    posts = Posts.objects.all().order_by('-date_posted')
    return render(request, 'blog/home.html', {'user': request.user, 'posts': posts})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')
