from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth
from .models import Posts, Comment, Profile, Notification
from .models import Posts as Post

from .forms import ProfileForm
import json



def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        uname = request.POST.get('uname')
        upassword = request.POST.get('upassword')
        user = authenticate(username=uname, password=upassword)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")
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

        user = User.objects.create_user(username=email, email=email, password=password, first_name=fullname)
        messages.success(request, "Account created! Please login.")
        return redirect('login')

    return render(request, 'blog/signup.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You’ve been logged out.")
    return redirect('login')



def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    posts = Posts.objects.all().order_by('-date_posted')
    return render(request, 'blog/home.html', {'posts': posts})


def create_post_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if title and content:
            Posts.objects.create(title=title, content=content, author=request.user, image=image)
            messages.success(request, "Post created successfully.")
            return redirect('explore')
    return render(request, 'blog/create_post.html')


def explore_view(request):
    q = request.GET.get('q', '')
    posts = Posts.objects.all().order_by('-date_posted')
    if q:
        posts = posts.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(author__first_name__icontains=q)
        )
    return render(request, 'blog/explore.html', {'posts': posts, 'q': q})


def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)  # only allow the author
    if request.method == "POST":
        post.delete()
        messages.success(request, "✅ Your post has been deleted successfully.")
        return redirect('home')  # or 'dashboard' if you want
    return render(request, 'blog/confirm_delete.html', {'post': post})



def post_detail_view(request, slug):
    post = get_object_or_404(Posts, slug=slug)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
            if request.user != post.author:
                Notification.objects.create(user=post.author, actor=request.user, verb='commented', target_post=post)
            messages.success(request, "Comment added.")
            return redirect('post_detail', slug=post.slug)

    return render(request, 'blog/post_detail.html', {'post': post})


def toggle_like(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=403)

    post = get_object_or_404(Posts, id=post_id)
    liked = False
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        liked = True
        if request.user != post.author:
            Notification.objects.create(user=post.author, actor=request.user, verb='liked', target_post=post)

    return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})



def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    user_posts = Posts.objects.filter(author=request.user).order_by('-date_posted')
    return render(request, 'blog/profile.html', {'form': form, 'posts': user_posts})



def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    monthly = (
        Posts.objects.annotate(month=TruncMonth('date_posted'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    labels = [m['month'].strftime('%b %Y') for m in monthly]
    data = [m['count'] for m in monthly]

    context = {'labels': json.dumps(labels), 'data': json.dumps(data)}
    return render(request, 'blog/dashboard.html', context)



def notifications_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    notes = request.user.notifications.order_by('-timestamp')
    return render(request, 'blog/notifications.html', {'notes': notes})
