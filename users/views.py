from django.urls import reverse
from blog.models import Blog
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("password2")
        
        if not username or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect(reverse('signup'))

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect(reverse('signup'))

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect(reverse('signup'))

        # Create user
        try:
            user = User.objects.create_user(username=username, password=password)
            messages.success(request, "Account created successfully! Please log in.")
            return redirect(reverse('login'))
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return redirect(reverse('signup'))

    return render(request, "users/signup.html")


def login_page(request):
    from blog.views import blog_list
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "Both username and password are required.")
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(blog_list)
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, "users/login.html")



@login_required(login_url='login')
def profile_page(request):
    user_posts = Blog.objects.filter(user=request.user).order_by('-created_at')  # Ensure ordering
    context = {
        'user': request.user,
        'blogs': user_posts,
    }
    return render(request, 'users/profile.html', context)



@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect(login_page)