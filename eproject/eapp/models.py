
from django.db import models
from django.contrib.auth.models import User

from autoslug import AutoSlugField

# Create your models here.
class Catagory(models.Model):
    name= models.CharField(max_length=40)
    image=models.ImageField(upload_to='catagoryImage/', blank=True, null=True)
    parrent=models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    title=models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
      return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=50)
    image=models.ImageField(upload_to='productImage/', blank=True, null=True)
    price=models.PositiveIntegerField()
    discount_price=models.PositiveIntegerField(blank=True, null=True)
    price_range=models.CharField(max_length=30, blank=True, null=True)
    description=models.TextField(max_length=100, blank=True, null=True)
    stock=models.IntegerField(blank=True, null=True)
    brand=models.CharField(max_length=30, blank=True, null=True)
    catagory=models.ForeignKey(Catagory, on_delete=models.CASCADE)
    slug=AutoSlugField(populate_from='name', unique=True, blank=True, null=True, default=None)
  

    verbose_name_plural ='Products'

    def __str__(self):
       return self.name
    

class Cart_product(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
       return self.product.name
    
class Order(models.Model):
   user=models.ForeignKey(User, on_delete=models.CASCADE)
   cart_product=models.ManyToManyField(Cart_product)
   start_data=models.DateTimeField(auto_now_add=True)
   ordered_data=models.DateTimeField(blank=True, null=True)
   ordered=models.BooleanField(default=False)

   def __str__(self):
      return self.user.username

    
    
