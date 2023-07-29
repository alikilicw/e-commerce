from email.headerregistry import Address
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify



class Address(models.Model):
    country = models.CharField(max_length=30, null= True, blank= True)
    state = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    neighbourhood = models.CharField(max_length=70, null=True, blank=True)
    full_address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.full_address}"

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to = "companies/profile_images", null=True, blank=True)
    cover_image = models.ImageField(upload_to = "companies/cover_images", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(blank=True, editable=False, unique=True, db_index=True, null=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    tax_num = models.CharField(max_length=10, unique=True, null=True, blank=True)
    tc = models.CharField(max_length=11, unique=True,null=True, blank=True)
    phone_num = models.CharField(max_length=12, null=True, blank=True)
    groups = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        _fname_lastname = self.first_name + self.last_name
        _fname_lastname = str(_fname_lastname).replace('ı', 'i')
        _name = str(self.name).replace('ı', 'i')
        if str(self.groups) != 'Normal User':
            if self.name is None and self.pk is not None:
                self.slug = slugify(_fname_lastname + " " + str(self.pk))
            elif self.name is not None: 
                self.slug = slugify(_name) 
        super().save(*args, **kwargs)