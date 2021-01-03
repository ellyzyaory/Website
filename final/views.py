from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, Http404
from .models import Product, Cart, CartItem, Checkout, UserAddress, EmailConfirmed
from django.urls import reverse
import re
import stripe
from .utils import id_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from .forms import LoginForm, RegistrationForm
from django.contrib import messages
from .forms import UserAddressForm
from django.conf import settings



# Create your views here.
# request for search
def search(request):
    try:
        q = request.GET.get('q')
    except:
        q = None
    if q:
        products = Product.objects.filter(title__icontains = q)
        context = {"query" : q, "products" : products}
        template = "results.html"
    else:
        template = "home.html"
        context = {}
    return render(request, template, context)

# request for home
def home(request):
    # Take all the products
    products = Product.objects.all()
    context = {"products" : products}
    template = "home.html"
    return render(request, template, context)

# request for menu
def menu(request):
    # Take all the products
    products = Product.objects.all()
    context = {"products" : products}
    template = "menu.html"
    return render(request, template, context)

# request for food ( single product )
def food(request, slug):
    try:
        product = Product.objects.get(slug = slug)
        images = product.productimage_set.all()
        context = {"product" : product, "images" : images}
        template = "food.html"
        return render(request, template, context)
    except:
        raise Http404

# request for order 
def order(request):
    try:
        the_id = request.session["cart_id"] 
        cart = Cart.objects.get(id = the_id)
    except:
        the_id = None
    if the_id:
        context = {"cart" : cart}
    else:
        empty_message = "There is currently no order"
        context = {"empty" : True, "empty_message" : empty_message}
    template = "order.html"
    return render(request, template, context)

# request for updating cart
def update_cart(request, slug):
    try:
        qty = request.GET.get("qty")
        update_qty = True
    except:
        qty = None
        update_qty = False

    try:
        the_id = request.session["cart_id"] 
    except:
        new_cart = Cart()
        new_cart.save()
        request.session["cart_id"] = new_cart.id
        the_id = new_cart.id

    cart = Cart.objects.get(id = the_id)

    try:
        product = Product.objects.get(slug = slug)
    except Product.DoesNotExist:
        pass
    except:
        pass

    cart_item, created = CartItem.objects.get_or_create(cart = cart, product = product)
    if created:
        print("yeah")
    if update_qty and qty:
        if int(qty) == 0: 
            cart_item.delete()
        else:
            cart_item.quantity = qty
            cart_item.save()
    else:
        pass
    # Starting value before any items are added into Order
    new_total = 0.000

    # Add the price of all the items that are added into Order
    for item in cart.cartitem_set.all():
        total_line = float(item.product.price) * item.quantity
        new_total += total_line

    # Count the number of items that is in the Order
    request.session["items_total"] = cart.cartitem_set.count()
    cart.total = new_total
    cart.save()
    return HttpResponseRedirect(reverse("order"))

try:
    stripe_pub = settings.STRIPE_PUBLISHABLE_KEY
    stripe_secret = settings.STRIPE_SECRET_KEY
except Exception as e:
    raise NotImplementedError(str(e))

stripe.api_key = stripe_secret

# request for order 2 
def order_2(request):
    context = {}
    template = "user.html"
    return render(request, template, context)

# to checkout, user needs to login
@login_required
# request for checkout
def checkout(request):
    try:
        the_id = request.session["cart_id"]
        cart = Cart.objects.get(id = the_id)
    except:
        the_id = None
        return HttpResponseRedirect(reverse("order"))

    # try if product exist, get the product
    try:
        new_checkout = Checkout.objects.get(cart = cart)
    except Checkout.DoesNotExist:
        new_checkout = Checkout()
        new_checkout.cart = cart
        new_checkout.user = request.user
        new_checkout.checkout_id = id_generator()
        new_checkout.final_amount = cart.total
        new_checkout.save()
    except:
        new_checkout = None
        return HttpResponseRedirect(reverse("order"))

    final_amount = 0
    if new_checkout is not None:
        new_checkout.sub_total = cart.total
        new_checkout.save()
        final_amount = new_checkout.get_final_amount()

    # Address
    try:
        address_added = request.GET.get("address_added")
 
    except:
        address_added = None

    if address_added is None:
        address_form = UserAddressForm()
    else:
        address_form = None

    if request.method == "POST":
        address_form = UserAddressForm(request.POST)
        if address_form.is_valid():
            new_address = address_form.save(commit = False)
            new_address.user = request.user
            new_address.save()
            address_form = UserAddressForm()
            return HttpResponseRedirect(reverse("checkout"))

    current_addresses = UserAddress.objects.filter(user = request.user)

    # Checkout using stripe
    if request.method == "POST":          
        try:
            user_stripe = request.user.userstripe.stripe_id
            customer = stripe.Customer.retrieve(user_stripe)
        except:
            customer = None
            pass
        if customer is not None:   
            token = request.POST.get('stripeSource')
            card = stripe.Customer.create_source(user_stripe, source = "tok_visa")
            charge = stripe.Charge.create(
                amount = int(final_amount * 100000),
                currency = "idr",
                card = card,
                customer = customer, 
                description = "Charge for %s" %(request.user.username),
                )
            if charge["captured"]:
                new_checkout.status = "Finished"
                new_checkout.save()
                del request.session["cart_id"]
                del request.session["items_total"]
                return HttpResponseRedirect(reverse("message_success"))

    context = {
    "checkout" : new_checkout,
    "address_form" : address_form, 
    "current_addresses" : current_addresses,
    "stripe_pub" : stripe_pub,
    }
    template = "checkout.html"
    return render(request, template, context)

# request for contact us
def contact(request):
    return render(request, "contact.html")

# request for about us
def about(request):
    return render(request, "about.html")

# request for logout
def logout_view(request):
    logout(request)
    messages.success(request, "Successfully Logged out.")
    return HttpResponseRedirect('%s'%(reverse("auth_login")))

# request for login
def login_view(request):
    form = LoginForm(request.POST or None)
    btn = "Login"
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username= username, password= password)
        login(request, user)
        messages.success(request, "Successfully Logged In. Welcome Back!")
        return HttpResponseRedirect("/")
    context = {
        "form" : form,
        "submit_btn" : btn,
    }
    return render(request, "login_form.html", context)

# request for registration form
def registration_view(request):
    form = RegistrationForm(request.POST or None)
    btn = "Join"
    if form.is_valid():
        new_user = form.save(commit = False)
        new_user.save()
        messages.success(request, "Successfully Registered. Please confirm your email now.")
        return HttpResponseRedirect("/")
        
    context = {
        "form" : form,
        "submit_btn" : btn,
    }
    return render(request, "register_form.html", context)


# activation view for confirming email
SHA1_RE = re.compile('^[a-f0-9]{40}$')
def activation_view(request, activation_key):
    if SHA1_RE.search(activation_key):
        print("activation key is real")
        try:
            user_confirmed = EmailConfirmed.objects.get(activation_key = activation_key)
        except EmailConfirmed.DoesNotExist:
            user_confirmed = None
            messages.success(request, "There was an error with you request.")
            return HttpResponseRedirect("/")
        if user_confirmed is not None and not user_confirmed.confirmed:
            page_message = "Confirmation Successful"
            user_confirmed.confirmed = True
            user.activation_key = "Confirmed"
            user_confirmed.save()
            messages.success(request, "Successfully Confirmed.")
        elif user_confirmed is not None and user_confirmed.confirmed:
            messages.success(request, "Already Confirmed.")
        else:
            pass
        context = {"page_message" : page_message}
        return render(request, "activation_complete.html", context)
    else:
        raise Http404

# success message
def message_success(request):
    return render(request, "message_success.html")
