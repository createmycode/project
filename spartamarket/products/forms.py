from django import forms
from .models import Product, Hashtag

class ProductForm(forms.ModelForm):
    hashtag_str = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs) 

    class Meta:
        model = Product
        fields = ['title', 'description', 'image', 'hashtag_str']

    def save(self, commit=True):
        product = super().save(commit=False)

        if self.user:
            product.user = self.user
        
        if commit:
            product.save()

        # 해시태그 처리
        hashtags_input = self.cleaned_data.get('hashtags_str', '')
        hashtags_list = [h for h in hashtags_input.replace(',', ' ').split() if h]
        new_hashtags = []
        for ht in hashtags_list:
            ht_obj, created = Hashtag.objects.get_or_create(name=ht)
            new_hashtags.append(ht_obj)

        product.hashtags.set(new_hashtags)

        if not commit:
            product.save()

        return product