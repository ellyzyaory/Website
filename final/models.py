from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from decimal import Decimal
import stripe



# Create your models here.

# Adding new product details in admin
class Product(models.Model):
    title = models.CharField(max_length = 120)
    description = models.TextField(null = True, blank = True)
    price = models.DecimalField(decimal_places = 3, max_digits = 100)
    sale_price = models.DecimalField(decimal_places = 3, max_digits = 100, null = True, blank = True)
    #image = models.FileField(upload_to = 'products/images', null = True)
    slug = models.SlugField(unique = True)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated = models.DateTimeField(auto_now_add = False, auto_now = True)
    active = models.BooleanField(default = True)

    def __unicode__(self):
        return str(self.title)

    class Meta:
        unique_together = ('title', 'slug') 

    def get_price(self):
        return self.price

    def get_absolute_url(self):
        return reverse("food", kwargs = {"slug": self.slug })

# Adding new product images in admin
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'products/images/')
    featured = models.BooleanField(default = False)
    thumbnail = models.BooleanField(default = False)
    active = models.BooleanField(default = True)
    updated = models.DateTimeField(auto_now_add = False, auto_now = True)

    def __unicode__(self):
        return self.product.title

# Cart item feature in admin
class CartItem(models.Model):
    cart = models.ForeignKey('Cart', null= True, blank = True, on_delete = models.CASCADE)
    # cart foreign key
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)
    total_line = models.DecimalField(default = 0.000, max_digits = 1000, decimal_places = 3)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated = models.DateTimeField(auto_now_add = False, auto_now = True)

    def __unicode__(self):
        try:
            return str(self.cart.id)
        except:
            return self.product.title

# Cart features in admin
class Cart(models.Model):
    total = models.DecimalField(decimal_places = 3, max_digits = 100, default = 0.000)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated = models.DateTimeField(auto_now_add = False, auto_now = True)
    active = models.BooleanField(default = True)

    def __unicode__(self):
        return "Cart id: %s" %(self.id)

# Status types
STATUS_CHOICES = (
    ("Started", "Started"),
    ("Abandoned", "Abandoned"),
    ("Finished", "Finished"),
)

try:
    tax_rate = settings.DEFAULT_TAX_RATE
except Exception as e:
    raise NotImplementedError(str(e))

# Checkout features in admin
class Checkout(models.Model):
    user = models.ForeignKey(User, blank = True, null = True, on_delete = models.CASCADE)
    checkout_id = models.CharField(max_length = 120, default = 'ABC', unique  = True)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    status = models.CharField(max_length = 120, choices = STATUS_CHOICES, default = "Started")
    # address
    sub_total = models.DecimalField(default = 0.000, max_digits = 1000, decimal_places = 3)
    tax_total = models.DecimalField(default = 0.000, max_digits = 1000, decimal_places = 3)
    final_total = models.DecimalField(default = 0.000, max_digits = 1000, decimal_places = 3)
    checkout_id = models.CharField(max_length = 120, default = 'ABC', unique = True)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated = models.DateTimeField(auto_now_add = False, auto_now = True)

    def __unicode__(self):
        return self.checkout_id

    def get_final_amount(self):
        instance = Checkout.objects.get(id = self.id)
        three_places = Decimal(1000) 
        instance.tax_total = Decimal(Decimal("%s"%(tax_rate)) * Decimal(self.sub_total)).quantize(three_places)
        instance.final_total = Decimal(self.sub_total) + Decimal(instance.tax_total)
        instance.save()
        return instance.final_total

# Userstripe features in admin
class UserStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    stripe_id = models.CharField(max_length = 120, null = True, blank = True)

    def __unicode__(self):
        return str(self.stripe_id)

# Email Confirmation features in admin
class EmailConfirmed(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    activation_key = models.CharField(max_length = 200, null = True, blank = True)
    confirmed = models.BooleanField(default = False)

    def __unicode__(self):
        return str(self.confirmed)

    def activate_user_email(self):
        activation_url = "%s%s" %(settings.SITE_URL, reverse("activation_view", args = [self.activation_key]))
        context = {
            "activation_key" : self.activation_key,
            "activation_url" : activation_url,
            "user" : self.user.username,
        }
        message = render_to_string("activation_message.txt", context)
        subject = "Activate your Email"
        self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    def email_user(self, subject, message, from_email = None, **kwargs):
        send_mail(subject, message, from_email, [self.user.email], kwargs)

# User address features in admin
class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    address = models.CharField(max_length = 120)
    address2 = models.CharField(max_length = 120, null = True, blank = True)
    city = models.CharField(max_length = 120)
    phone_number = models.CharField(max_length = 120)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated = models.DateTimeField(auto_now_add = False, auto_now = True)

    def __unicode__(self):
        return str(self.user.username)

    # get the address and city
    def get_address(self):
        return "%s, %s" %(self.address, self.city)
