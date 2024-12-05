from .models import Category  # Adjust the import based on your project structure

def categories_processor(request):
    # This function returns a dictionary of categories
    categories = Category.objects.all()  # Fetch all categories
    return {'categories': categories}
             