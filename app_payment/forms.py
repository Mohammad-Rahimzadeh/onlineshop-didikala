from django import forms

class updateBasketItemForm(forms.Form):
    item_id = forms.IntegerField(widget=forms.HiddenInput())
    count = forms.IntegerField(min_value=1, label="تعداد")