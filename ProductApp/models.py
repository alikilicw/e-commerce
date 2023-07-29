import re
from django.db import models
from django.utils.text import slugify
from Account.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, editable=False, unique=True, db_index=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
class Currency(models.Model):
    currency_type = models.CharField(max_length=50, null=True, blank=True)
    currency_symbol = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return f"{self.currency_type}"


class Product(models.Model):
    name = models.CharField(max_length=200)
    image1 = models.ImageField(upload_to = "products", null=True, blank=True)
    image2 = models.ImageField(upload_to = "products", null=True, blank=True)
    image3 = models.ImageField(upload_to = "products", null=True, blank=True)
    description = models.TextField()
    price = models.CharField(max_length=9, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(blank=True, editable=False, unique=True, db_index=True, max_length=150)
    category = models.ManyToManyField(Category)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    fav_user = models.ManyToManyField(CustomUser, related_name="fav_user", blank=True)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.name}"

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        prod_name = self.name
        prod_name = str(prod_name).replace('ı', 'i')

        self.slug = slugify(prod_name)
        super().save(*args, **kwargs)

class Review(models.Model):
    to_user = models.ForeignKey(CustomUser,blank=True, on_delete=models.CASCADE, null=True, related_name="to_user")
    product = models.ForeignKey(Product, blank=True,on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name="from_user")
    is_active = models.BooleanField(default=False)
    review_text = models.TextField(null=True)
    review_date = models.DateField(auto_now_add=True, null=True)
