from django import forms
from app_social.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('title' , 'body' , 'rate' , 'strength' , 'weakness' , 'is_suggest')
        
        
# class PointForm(forms.ModelForm):
#     class Meta:
#         model = Point
#         fields = ['strength', 'weakness']