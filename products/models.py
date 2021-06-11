from django.db import models
from django.contrib.auth.models import User
from account.models import UserProfile
from sellers.models import Seller
import uuid
from django.contrib.auth.models import Permission



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):

    seller=models.ForeignKey(Seller,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=100)
    category = models.ManyToManyField(Category, related_name='category')
    description = models.TextField(max_length=1000)
    price = models.IntegerField(default=0)
    rating = models.ManyToManyField(User, blank=True, related_name='rating')

    class Meta:
        permissions = (
           ("can_add_product","can add product"),
        )

    def __str__(self):
        return self.name

    def get_image_filename(instance, filename):
        name = name.product.title
        slug = slugify(name)
        return "images/productimages/%s-%s" % (slug, filename)

    @property
    def rating_count(self):
        return (self.rating.count())

    @property
    def sorted_image_set(self):
        return self.product_images.order_by('time_created')


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.FileField(upload_to='images/productimages/',
                             default='images/productimages/dummy.png', blank=True)
    time_created = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.product.name


class BillingAddress(models.Model):
    name = models.CharField(max_length=50)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField()

    def __str__(self):
        return self.address1


class OrderDetail(models.Model):
    ord_id=uuid.uuid4().hex[:6].upper()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField( max_length=15, unique=True, default=ord_id, editable=False)
    orderStatus = models.BooleanField(default=False)
    cancelStatus = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.FloatField(default=0, blank=True, null=True)
    address = models.ForeignKey(BillingAddress, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    paid_unpaid =models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)
