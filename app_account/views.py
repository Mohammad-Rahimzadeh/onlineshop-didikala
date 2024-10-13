from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from app_account.forms import editProfileForm , editUserForm , SignupForm , addressForm , changePasswordForm
from app_account.models import Profile , Address , Favorite , FavoriteProduct
from app_store.models import Product

# Create your views here.



# ================================================== loginView ======================================================= #


def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request , username = username , password = password)
        if user is not None:
            login(request , user)
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get('next'))
            return redirect('home')
        else:
            error_message = 'نام کاربری یا رمز عبور اشتباه است. مجددا تلاش کنید.'
            context = {
                'error_message':error_message
            }
            return render(request , 'app_account/login.html' , context)
            
    else:   
        return render(request , 'app_account/login.html')


# ================================================== signupView ======================================================= #


def signupView(request):
    context = {}
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username = form.cleaned_data['username'],
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password'],
            )
            user.save()
            
            profile = Profile(
                user = user,
                phone_number = form.cleaned_data['phone_number'],
            )
            profile.save()
            
            login(request, user)
            return redirect('welcome')
    else:
        context['form'] = SignupForm()
    return render(request, 'app_account/signup.html', context)


# ================================================== welcomeView ======================================================= #


@login_required
def welcomeView(request):
    return render(request , 'app_account/welcome.html')


# ================================================== profileView ======================================================= #


@login_required
def profileView(request):
    try:
        profile = request.user.profile
        
        favorite = Favorite.objects.get(user=request.user)
        favorite_products = favorite.favorite_products.all()
        
        context = {
            'profile': profile,
            'favorite_products': favorite_products
        }
        return render(request, 'app_account/profile.html', context)
        
    except Favorite.DoesNotExist:
        context = {
            'profile': request.user.profile
        }
        return render(request, 'app_account/profile.html', context)
        
    except:
        if request.user.profile.phone_number:
            context={
                'profile':request.user.profile
            }
            return render(request , 'app_account/profile.html' , context)
        else:
            complete_profile_message = 'حساب کاربری خود را تکمیل کنید'
            context={
                'complete_profile_message':complete_profile_message
            }
            return render(request , 'app_account/edit-profile.html' , context)


# ================================================== editProfileView ======================================================= #


def editProfileView(request):
    if request.method == 'POST':
        profile_edit_form = editProfileForm(request.POST , request.FILES , instance=request.user.profile )
        user_edit_form = editUserForm(request.POST , instance=request.user)
        if profile_edit_form.is_valid() and user_edit_form.is_valid():
            profile_edit_form.save()
            user_edit_form.save()
        context ={
            'profile_edit_form' : profile_edit_form ,
            'user_edit_form' : user_edit_form ,
            } 
        return redirect('profile')
    
    else:
        profile_edit_form = editProfileForm(instance=request.user.profile)
        user_edit_form = editUserForm(instance=request.user)
        
        context ={
            'profile_edit_form' : profile_edit_form ,
            'user_edit_form' : user_edit_form ,
            'profile_image' : request.user.profile.image ,
            } 
    return render(request , 'app_account/edit-profile.html' , context)
        

# ================================================== logoutView ======================================================= #


def logoutView(request):
    logout(request)
    return redirect('login')

# ================================================== privacyView ======================================================= #


def privacyView(request):
    return render(request , 'app_account/page-privacy.html')


# ================================================== personalInfoView ======================================================= #


@login_required
def personalInfoView(request):
    return render(request , 'app_account/profile-personal-info.html')



# ================================================== profileFavorites ======================================================= #


@login_required
def profileFavoritesView(request):
    favorite = Favorite.objects.filter(user=request.user).first()
    
    if not favorite:
        favorite = Favorite.objects.create(user=request.user)
    
    favorite_products = FavoriteProduct.objects.filter(favorite=favorite)
    
    context = {
        'favorite_products':favorite_products ,
    }
    
    return render(request , 'app_account/profile-favorites.html' , context)




# ==================================================  addToFavoriteView  ================================================= #


@login_required
def addToFavoriteView(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    favorite, created = Favorite.objects.get_or_create(user=request.user)
    
    favorite_product, created = FavoriteProduct.objects.get_or_create(favorite=favorite, product=product)
    
    return redirect('favorites')




# ==================================================  removeFromFavoriteView  ================================================= #


@login_required
def removeFromFavoriteView(request, item_id):
    favorite_product = get_object_or_404(FavoriteProduct, id=item_id)
    favorite_product.delete()
    return redirect('favorites')


# ================================================== profileAddressView ======================================================= #


@login_required
def profileAddressView(request):
    profile = request.user.profile
    profile_addresses = request.user.profile.addresses.all()

    context={
        'profile':profile ,
        'profile_addresses':profile_addresses ,
    }
    return render(request , 'app_account/profile-addresses.html' , context)



# ================================================== addAddressView ======================================================= #



@login_required
def addAddressView(request):
    if request.method == 'POST':
        form = addressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.profile = request.user.profile
            address.save()
            return redirect('addresses')
    else:
        form = addressForm()
        
    context={
        'form': form
    }
    return render(request, 'app_account/add-address.html', context)



# ==================================================  editAddressView  ================================================= #



@login_required
def editAddressView(request, address_id):
    address = get_object_or_404(Address, id=address_id, profile=request.user.profile)
    
    if request.method == 'POST':
        form = addressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('addresses')
    else:
        form = addressForm(instance=address)

    context={
        'form': form
    }
    return render(request, 'app_account/edit-address.html', context)



# ==================================================  removeAddressView  ================================================= #


@login_required
def removeAddressView(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    address.delete()
    return redirect('addresses')



# ================================================== profileCommentsView ======================================================= #


@login_required
def profileCommentsView(request):
    user_comments = request.user.user_comments.all()
    context={
        'user_comments':user_comments
    }

    return render(request , 'app_account/profile-comments.html' , context)




# ================================================== changePasswordView ======================================================= #


@login_required
def changePasswordView(request):
    context = {}
    if request.method == 'POST':
        user=request.user
        form = changePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password1 = form.cleaned_data['new_password1']    
            new_password2 = form.cleaned_data['new_password2']
            if not user.check_password(old_password):
                massage = 'رمز عبور قبلی خود را اشتباه وارد کردید!'
            elif new_password1 != new_password2:
                massage = 'رمز عبور جدید شما با هم مطابقت ندارد!'
            else:
                user.set_password(new_password1)
                user.save()
                login(request , user)
                return redirect('profile')
            context['massage'] = massage
    else:
        form = changePasswordForm()

    context['form'] = form
    return render(request , 'app_account/password-change.html' , context)

            