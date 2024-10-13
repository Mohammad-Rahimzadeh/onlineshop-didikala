from django.shortcuts import render , get_object_or_404 , redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Product , Banner , Brand , Category
from app_account.models import Favorite

# Create your views here.


# ================================================ notFoundView ============================================ #


def notFoundView(request):
    return render(request , 'app_store/404.html')


# ================================================ homeView ============================================ #


def homeView(request):
    banners = Banner.objects.filter(title__in=['main-slider', 'sidebar-banner', 'medium-banner', 'small-banner' , 'large-banner'])
    banner_dict = {banner.title: banner.images for banner in banners}

    brand = Brand.objects.filter(is_available=True, show_brand=True)
    
    products = Product.objects.filter(is_published=True)
    
    product_counter = 0
    for product in products:
        product_counter += 1
        
    context = {
        'main_slider': banner_dict.get('main-slider'),
        'sidebar_banner': banner_dict.get('sidebar-banner'),
        'medium_banner': banner_dict.get('medium-banner'),
        'small_banner': banner_dict.get('small-banner'),
        'large_banner': banner_dict.get('large-banner'),
        'products' : products,
        'brand' : brand,
        'product_counter' : product_counter,
    }
    
    return render(request , 'app_store/home.html' , context)


# ================================================ productListView ============================================ #


def productListView(request):
    all_products = Product.objects.all()
    
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            all_products = Product.objects.filter(name_fa__icontains = keyword)
        else:
            all_products = Product.objects.filter(is_published=True)
    else:
        all_products = Product.objects.filter(is_published=True)
        
    paginator = Paginator(all_products , 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)    

    context = {
        'all_products' : all_products,
    }
    
    return render(request , 'app_store/all-products.html' , context)

# ================================================ productDetailView ============================================ #

        
def productDetailView(request , id):
    single_product = get_object_or_404(Product, id=id)
    single_product.visit_count += 1
    single_product.save()
    
    comments = single_product.products_comment.filter(is_published=True)
    
    colors = single_product.product_color.all()

    context = {
        'single_product': single_product ,
        'comments': comments ,
        'colors': colors ,
    }

    if single_product.count > 0:
        return render(request, 'app_store/product-detail.html', context)
    else:
        return render(request, 'app_store/single-product-not-available.html', context)



# ================================================ brandsView ============================================ #



def brandsView(request, slug):
    try:
        brands = Brand.objects.get(slug=slug)
    except Brand.DoesNotExist:
        return render(request, 'app_store/404.html')
    
    product_by_brand = Product.objects.filter(brand=brands)

    context = {
        'brands': brands,
        'product_by_brand': product_by_brand,
    }

    return render(request, 'app_store/product_by_brand.html', context)



# ================================================ categoryView ============================================ #



def categoryView(request, slug):
    try:
        categories = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return render(request, 'app_store/404.html')
    
    product_by_category = Product.objects.filter(category=categories)

    context = {
        'categories': categories,
        'product_by_category': product_by_category,
    }

    return render(request, 'app_store/product_by_category.html', context)




# ================================================ productFilterView ============================================ #

        

def productFilterView(request):
    # دریافت تمام محصولات
    products = Product.objects.filter(is_published=True)

    # فیلتر بر اساس جستجو (نام محصول یا برند)
    query = request.GET.get('s')
    if query:
        products = products.filter(name_fa__icontains=query) | products.filter(brand__title__icontains=query)

    # فیلتر بر اساس دسته‌بندی‌ها
    categories = request.GET.getlist('category')
    if categories:
        products = products.filter(category__id__in=categories)

    # فیلتر بر اساس برند
    brands = request.GET.getlist('brand')
    if brands:
        products = products.filter(brand__id__in=brands)

    # فیلتر بر اساس فروشنده
    seller = request.GET.get('seller')
    if seller:
        products = products.filter(seller__icontains=seller)

    # فیلتر بر اساس رنگ
    colors = request.GET.getlist('color')
    if colors:
        products = products.filter(product_color__id__in=colors)

    # فیلتر بر اساس وضعیت موجود بودن کالا
    available = request.GET.get('available')
    if available == 'on':
        products = products.filter(is_published=True)

    # فیلتر بر اساس قیمت (در صورت داشتن فیلد قیمت)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    context = {
        'products': products,
    }
    return render(request, 'app_store/all-products.html', context)