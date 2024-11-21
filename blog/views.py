from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required



def blog_list(request):
    context = {}
    try:
        blogs = Blog.objects.all()
        # category = Category.objects.all()
        context['blogs']=blogs
        # context['category']=category
    except Exception as e:
        return HttpResponse(str(e))
    return render(request, "blogs/show_blog.html", context)


def get_blog(request, id):
    context = {}
    try:
        blog = Blog.objects.get(id=id)
        context['blog'] = blog

    except Blog.DoesNotExist:
        return HttpResponse("Blog not found")
    return render(request, "blogs/blog_details.html", context)


def get_cat(request, id):
    context = {}
    try:
        
        blogs = Blog.objects.filter(category=Category.objects.filter(id=id)[0])
        # print(blogs.title)
        context['blogs'] = blogs

    except Blog.DoesNotExist:
        return HttpResponse("Blog not found")
    return render(request, "blogs/show_blog.html", context)


@login_required(login_url='login')
def add_blog(request):
    if request.method == "POST":
        # Get form data
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")  # Use FILES for uploaded files
        category_id = request.POST.get("category")
        
        # Get the category object
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, "Invalid category selected!")
            return redirect("add_blog")  # Redirect to the same page if the category is invalid

        # Create the blog object
        blog = Blog.objects.create(
            title=title,
            content=content,
            category=category,
            user=request.user,
            image=image if image else None
        )
        
        # Save is not required here because `objects.create` already saves the object
        messages.success(request, "Blog added successfully!")
        return redirect("profile_page")  # Replace 'profile_page' with the appropriate URL name

    # Render the form template
    return render(request, "blogs/add_blog.html")


@login_required(login_url='login')
def update(request, id):
    # Get the blog object or return a 404 if not found
    post = Blog.objects.get( id=id)
    context = {"post"}

    if request.method == "POST":
        # Get form data
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")  # Use FILES for uploaded files
        category_id = request.POST.get("category")

        # Update the blog instance
        print(category_id)
        post.title = title
        post.content = content
        post.category = Category.objects.get(id=category_id)
        if image:  
            post.image = image
       

    
        post.save()

        messages.success(request, "Blog updated successfully!")
        return redirect("profile_page")  # Replace 'profile_page' with the appropriate URL name

    # Render the form template with existing post data
    return render(request, "blogs/add_blog.html", {"blog": post})




def delete(request, id):
    from users.views import profile_page
    post = Blog.objects.get(id=id)
    post.delete()
    return redirect(profile_page)



def blog_list_search(request):
    query = request.GET.get("search", "")
    blogs = Blog.objects.all()
    
    # Filter blogs if a search query is provided
    if query:
        blogs = blogs.filter(title__icontains=query) | blogs.filter(content__icontains=query)
    
    return render(request, "blogs/show_blog.html", {"blogs": blogs, "query": query})


