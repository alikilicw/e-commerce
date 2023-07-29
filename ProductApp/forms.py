from django import forms 
from .models import Product

class AddProductForm(forms.ModelForm):
    class Meta: 
        model = Product
        fields = ('name', 'price', 'currency', 'category', 'image1', 'image2', 'image3', 'description')