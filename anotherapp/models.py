from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.


class Settings(models.Model):
    user = models.OneToOneField(User)  # IMPORT THE USER FOR SECURITY CHECKS LATER
    deliveryMin = models.DecimalField(max_digits=5, decimal_places=2, help_text="What is the smallest dollar amount to be able to deliver?", default=10)
    tax = models.DecimalField(max_digits=5, decimal_places=4, help_text="Tax as decimal (8.65% is 0.0865)", default=.0863)
    deliveryFee = models.DecimalField(max_digits=5, decimal_places=2, help_text="How much is it additionally to deliver?", default=2.50)
    sKey = models.CharField(max_length=100)
    site_title = models.CharField(max_length=100, help_text="What is the website called?", default="website title", null=True, blank=True)
    site_description = models.CharField(max_length=250, help_text="Give a description seen in the stripe checkout modal.", default="website description", null=True, blank=True)

    def __str__(self):
        return '%s' % (self.user)


class Product(models.Model):
    image = models.ImageField(default=0, blank=True)
    name = models.CharField(max_length=255, help_text="What is The Name To Display For The Product?")
    price = models.FloatField(help_text="Add The Price WITHOUT The $ Sign. Such As: 4.95 or 9.99")
    keywords = models.CharField(max_length=255, help_text="Enter Keywords Seperated By Spaces Such As: chicken, rice, hot, peppers")
    category = models.ForeignKey('Category', help_text="Choose a Category. If you would like to add a Category, go back and find the Category page",
                                 default=0, null=True, blank=True)
    sizes = models.CharField(max_length=255, help_text="To Make Different Sizes Type: \"Small,Medium,Large\" Without Any Spaces")
    featured = models.IntegerField(default=0, null=True, blank=True, help_text="Set This To 1 For It To Display on The Front Page")
    description = models.TextField(max_length=1500)
    excerpt = models.CharField(max_length = 100, help_text="This is a Short Snippet Below Each Product")

    def __str__(self):
        return self.name

    def sizes_as_list(self):
        return self.sizes.split(':')[0].split(',')

    def prices_as_list(self):
        return self.sizes.split(':')[1].split(',')

    def get_absolute_url(self):
        return reverse("update", kwargs={'pk': self.pk})


class CartItem(models.Model):
    belongs_to_cart = models.ForeignKey('Cart', null=True, blank=True, default=False)
    product = models.ForeignKey(Product)
    size = models.CharField(max_length=255, default=0)
    quantity = models.IntegerField(default=0)
    total = models.FloatField()

    def __str__(self):
        return '%s' % self.product


class Cart(models.Model):
    total = models.CharField(max_length=10, default=0)
    session = models.CharField(max_length=35, default=0)
    created_on = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now_add=False, auto_now=True, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % self.session


class Order(models.Model):
    # THIS MODEL IS FOR THE ADMIN AND CUSTOMER TO VIEW ORDER INFORMATION
    orderName = models.ForeignKey(User, default=False, null=True, blank=True)
    order_cart = models.ForeignKey(Cart, max_length=45, default=False, null=True, blank=True)
    total = models.FloatField()
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(null=True, default=0)
    confirmation = models.CharField(max_length=15, default=0)
    delivery = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return '%s - %s' % (self.orderName, self.total)

    class Meta:
        ordering = ['-date']


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    featured = models.BooleanField()

    def __str__(self):
        return self.category_name
