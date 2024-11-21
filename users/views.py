
from blog.models import Blog
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required




def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        print(username, password, password2)

        # Check if passwords match
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect(signup)

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
            return redirect(signup)

        # Create the user and set the hashed password
        user = User(username=username)
        user.set_password(password)  # Use the actual password variable here
        user.save()

        messages.success(request, "Account created successfully! Please log in.")
        return redirect(login_page)

    return render(request, "users/signup.html")




def login_page(request):
    from blog.views import blog_list
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.get(username=username)
        print(f"User found: {user.username}")
        user = authenticate(request, username=username , password=password)
        print(username, password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect(blog_list)
        else:
            messages.error(request, "User not found")
            return redirect(login_page)
    return render(request, "users/login.html")





@login_required(login_url='login')
def profile_page(request):
    # Get the logged-in user's details
    user = request.user
    # Get all posts created by the logged-in user
    user_posts = Blog.objects.filter(user=user)
    
    context = {
        'user': user,
        'blogs': user_posts,
    }
    return render(request, 'users/profile.html', context)




@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect(login_page)

