from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app_store.models import Product
from app_social.forms import CommentForm
from .models import Comment , IsUsefull




# Create your views here.

@login_required
def addCommentView(request , id):
    single_product = get_object_or_404(Product, id=id)
    comments = single_product.products_comment.filter(is_published=True)
    new_comment = None
    new_point = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        # point_form = PointForm(request.POST)
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = single_product
            new_comment.user = request.user
            new_comment.save()
            
            # new_point = point_form.save(commit=False)
            # new_point.comment = new_comment
            return redirect('product_detail', id=single_product.id)
    else:
        comment_form = CommentForm()
        # point_form = PointForm()
    
    context = {
        'single_product' : single_product ,
        'comments' : comments ,
        'new_comment' : new_comment ,
        'comment_form' : comment_form ,
        # 'point_form' : point_form
    }
    return render(request , 'app_social/add-comment.html' , context)




@login_required
def deleteCommentView(request , comment_id):
    comment = get_object_or_404(Comment , id=comment_id)
    comment.delete()
    return redirect('comments')




@login_required
def vote_comment(request, comment_id , product_id):
    single_product = get_object_or_404(Product, id=product_id)
    comment = get_object_or_404(Comment, id=comment_id)

    # کاربر نباید برای کامنت خودش رای بدهد
    if comment.user == request.user:
        messages.error(request, 'You cannot vote on your own comment.')
        return redirect('product_detail', id=single_product.id)  # نام ویوی مربوط به صفحه‌ی قبلی یا لیست کامنت‌ها
    
    # مقدار لایک یا دیسلایک از درخواست POST گرفته می‌شود
    is_useful = request.POST.get('is_useful')

    # بررسی اینکه مقدار is_useful درست ارسال شده باشد
    if is_useful is None or is_useful not in ['true', 'false']:
        messages.error(request, 'Invalid vote.')
        return redirect('product_detail', id=single_product.id)

    # تبدیل مقدار is_useful به نوع Boolean
    is_useful = True if is_useful == 'true' else False

    # بررسی اینکه آیا کاربر قبلاً برای این کامنت رأی داده است یا نه
    vote, created = IsUsefull.objects.get_or_create(comment=comment, user=request.user)

    if not created:  # اگر کاربر قبلاً رأی داده باشد
        if vote.is_useful == is_useful:
            messages.info(request, 'You have already voted this way.')
        else:
            # اگر رأی کاربر متفاوت از رأی قبلی باشد، آن را به‌روز می‌کنیم
            if is_useful:  # لایک
                comment.like_count += 1
                comment.dislike_count -= 1 if comment.dislike_count > 0 else 0  # دیسلایک را کم می‌کنیم
            else:  # دیسلایک
                comment.dislike_count += 1
                comment.like_count -= 1 if comment.like_count > 0 else 0  # لایک را کم می‌کنیم

            vote.is_useful = is_useful
            vote.save()
            comment.save()  # ذخیره تغییرات در کامنت
            messages.success(request, 'Your vote has been updated.')
    else:
        # ایجاد رای جدید
        vote.is_useful = is_useful
        if is_useful:  # اگر لایک باشد
            comment.like_count += 1
        else:  # اگر دیسلایک باشد
            comment.dislike_count += 1
        vote.save()
        comment.save()  # ذخیره تغییرات در کامنت
        messages.success(request, 'Your vote has been submitted.')

    # بازگشت به همان صفحه یا صفحه‌ای که کامنت‌ها نمایش داده می‌شود
    return redirect('product_detail', id=single_product.id)  # نام ویوی مربوط به صفحه‌ی قبلی یا لیست کامنت‌ها