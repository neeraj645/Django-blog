from django.contrib import admin
from .models import Category, Blog

admin.site.register(Category)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display=['title','user', 'category','created_at',"updated_at"]
