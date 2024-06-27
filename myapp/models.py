from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
import random

class CustomUser(AbstractUser):
    mobile_number = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(unique=True)

    

    # def __str__(self):
    #     return self.username
class Categories(models.Model):
    name=models.CharField( max_length=50)
    image=models.ImageField( null=True,blank=False,upload_to='media/img')
    @property
    def get_imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    

    class Meta:
        verbose_name = ("Categories")
        verbose_name_plural = ("Categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Categories_detail", kwargs={"pk": self.pk})
    
class Product(models.Model):
    name=models.CharField( max_length=500)
    CategoriesId=models.ForeignKey(Categories, on_delete=models.CASCADE,null=True)
    image=models.JSONField(default=list)
    price=models.FloatField()
    discount=models.FloatField()
    discounted_price = models.FloatField(null=True, blank=True)
    brand=models.CharField(max_length=20)
    description=models.TextField()
    rating=models.IntegerField(null=True)
    createdDate=models.DateField(auto_now_add=True)
    availability=models.IntegerField(blank=True)
    is_new=models.BooleanField(default=True)
    
    
    def save(self, *args, **kwargs):
        # Calculate and set the discounted price before saving
        self.discounted_price = self.price - (self.price * self.discount / 100)
        super().save(*args, **kwargs)
    


    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})


class Cart(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    createdDate=models.DateField(auto_now_add=True)

    
    def __str__(self):
        return f"{self.user.username} - {self.createdDate}- {self.user.email}"
    
class Cart_item(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return  str(self.id) +" " + self.cart.user.username.upper() + " (" + self.product.name[:20]+")"

class BillingAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.first_name + " " + self.last_name + "-" + self.user.email + "-" + self.address + "-" + self.city +"-"+self.state +"-"+self.country +"-"+self.pincode
        
    

class ShippingAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    

    class Meta:
        verbose_name = ("ShippingAddress")
        verbose_name_plural =("ShippingAddresss")

    def __str__(self):
        return self.first_name + " " + self.last_name + "-" + self.user.email + "-" + self.address + "-" + self.city +"-"+self.state +"-"+self.country +"-"+self.pincode
        

    def get_absolute_url(self):
        return reverse("ShippingAddress_detail", kwargs={"pk": self.pk})

class Order(models.Model):
    # @staticmethod
    def generate_unique_order_id():
        return random.randint(10000, 99999)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    orderId = models.CharField(default=generate_unique_order_id, max_length=5, editable=False, unique=True)
    createdDate=models.DateTimeField(auto_now_add=True ,blank=True,null=True)
    shippingAddress=models.ForeignKey(ShippingAddress , on_delete=models.CASCADE ,blank=True,null=True)
    billingAddress=models.ForeignKey(BillingAddress , on_delete=models.CASCADE,blank=True,null=True)
    amount=models.FloatField(null=True,blank=True)
    
    

    def __str__(self):
        return f"{self.orderId}- {self.user.username} - {self.createdDate}"
    
class OrderLine(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.FloatField()

    def __str__(self):
        return  self.order.user.username + " " + self.product.name

class Wishlist(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " " + self.product.name
    
    
