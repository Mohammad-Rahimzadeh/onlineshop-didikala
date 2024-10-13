from app_store.models import Category

def categories_processor(request):
    category = Category.objects.filter(is_available=True)
    return {
        'category': category
    }
    