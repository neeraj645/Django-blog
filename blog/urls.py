from django.urls import path
from .views import blog_list, get_blog, get_cat, update, delete, blog_list_search, add_blog

urlpatterns = [
    path('', blog_list, name="blog_list"),  # Root path for blog app
    path('blogs/search/', blog_list_search, name='blog_list_search'),
    path('blogs/<int:id>/', get_blog, name='get_blog'),
    path('blogs/<int:id>/update/', update, name="update"),
    path('blogs/<int:id>/delete/', delete, name="delete"),
    path('categories/<int:id>/blogs/', get_cat, name="get_cat"),
    path('add_blog/',add_blog, name="add_blog")
]
