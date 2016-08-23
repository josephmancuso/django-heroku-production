from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import Http404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist, ViewDoesNotExist

from .forms import LoginForm, NewUserForm
from .models import Product, Cart, Order, Settings, CartItem
from django.db.models import Sum
import uuid  # uuid is used to create the session ID. Example around line 16



def index(request):
    if 'session_id' not in request.session:
        request.session['session_id'] = uuid.uuid4().hex[:35]
        query = Cart(session=request.session['session_id'], active=True)
        query.save()

    session = "%s" % request.session['session_id']

    # This block of code checks to see if there is a cart for the current session. If not, it creates a cart.
    # A cart is created for every user who does not yet have a session
    get_cart = Cart.objects.filter(session=session).exists()
    if get_cart:
        get_cart = Cart.objects.get(session=session)
    else:
        del request.session['session_id']
        request.session['session_id'] = uuid.uuid4().hex[:35]
        query = Cart(session=request.session['session_id'], active=True)
        query.save()
        get_cart = Cart.objects.filter(session=session)

    # Get all the featured products
    featured = Product.objects.filter(featured=1)

    # Check if there are any items in the cart, if there isnt, then send None as the cart's context variable
    cart = CartItem.objects.filter(belongs_to_cart=get_cart)
    if not cart.exists():
        cart = None

    # Get all the settings from the admins database.
    db_settings = Settings.objects.get(id=1)

    # This renders the home page
    return render(request, 'anotherapp/index.html',
                  {'featured': featured, 'cart': cart, 'session': session, 'settings': db_settings})


# This is the view for the category page. /app/view/ by default
def cat(request):
    if 'session_id' not in request.session:
        request.session['session_id'] = uuid.uuid4().hex[:35]

    # Get the session ID of the user
    session = request.session['session_id']

    # Get all items with a category. the __gt=0 is checking of the store owner set the category to anything
    cat = Product.objects.filter(category__gt=0)

    # Get the cart contents. Try to make this code shorter in future releases.
    get_cart = Cart.objects.get(session=session)
    cart = CartItem.objects.filter(belongs_to_cart=get_cart)
    if not cart.exists():
        cart = None

    # Get the database settings for the cart. This variable contains the delivery charge.
    db_settings = Settings.objects.get(id=1)

    return render(request, "anotherapp/cat.html", {"cat": cat, "cart": cart, 'settings': db_settings})


def viewMenu(request):
    # This renders the full menu of the website.
    if 'session_id' not in request.session:
        request.session['session_id'] = uuid.uuid4().hex[:35]

    session = request.session['session_id']
    chicken = Product.objects.filter(keywords__icontains='chicken')  # Get the products containing this keyword
    steak = Product.objects.filter(keywords__icontains='steak')  # Get the products containing this keyword
    no_image = Product.objects.filter(image='')  # Get the products that contain no images

    db_settings = Settings.objects.get(id=1)

    get_cart = Cart.objects.get(session=session)
    cart = CartItem.objects.filter(belongs_to_cart=get_cart)
    if not cart.exists():
        cart = None

    return render(request, 'anotherapp/view.html',
                  {'steak': steak, 'chicken': chicken, 'noimage': no_image, 'cart': cart, "settings": db_settings})


def product(request):
    # This will render individual products. This will most likely be optional and may or may not make it to production
    return render(request, 'anotherapp/view.html')


def add_to_cart(request):
    # Add items to the cart in the database
    if request.method == 'POST':
        '''
        A session variable is set when the user goes to the page, if there is somehow no session that exists when the
        user attempts to add something to the cart (something that will mess up if the session id doesnt exist) then
        create it here. This is just a fallback. The session is made in previous steps before this.
        '''
        if 'session_id' not in request.session:
            request.session['session_id'] = uuid.uuid4().hex[:35]

        products = request.POST.get('product', '')
        size = request.POST.get('size', '')
        quantity = request.POST.get('quantity', '')
        products = Product.objects.get(name=products)
        total = products.price * int(quantity)
        session_id = request.session['session_id']

        cart = Cart.objects.get(session=session_id)

        query = CartItem(product=products, size=size, quantity=quantity, total=total, belongs_to_cart=cart)
        query.save()

    return HttpResponse('')


def remove_from_cart(request):
    if request.method == "POST":
        session_id = request.session['session_id']
        quantity = request.POST.get('quantity')
        id = request.POST.get('id')



def login_user(request):
    # Login the user

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():

            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            email = request.POST.get('email', '')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/crm/')
    else:
        form = LoginForm()
    return render(request, 'anotherapp/login.html', {'form': form})


def logout_user(request):
    # Logout the user
    logout(request)
    return HttpResponseRedirect('/crm/login/')


def dashboard(request):
    username = None

    if request.user.is_authenticated():
        username = request.user.id

    dash_orders = Order.objects.filter(orderName=username, status__lt=4)
    dash_prev_orders = Order.objects.filter(orderName=username, status__gt=3).order_by('-date')

    return render(request, 'anotherapp/dashboard.html', {'dash_orders': dash_orders, 'prev_orders': dash_prev_orders})


def create_user(request):
    # Create a new user
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            email = request.POST.get('email', '')
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/crm/dashboard/')
    else:
        form = NewUserForm()
    return render(request, 'anotherapp/create.html', {'form': form})


def checkout(request):
    if 'session_id' not in request.session:
        request.session['session_id'] = uuid.uuid4().hex[:35]

    # Get the session for the user to search in the cart for their items
    session = request.session['session_id']

    # Get all items from the users cart to display on the checkout page

    db_settings = Settings.objects.get(id=1)

    cart = Cart.objects.filter(session=session)
    cart_items = CartItem.objects.filter(belongs_to_cart=cart)

    # Get the stripe token
    stripe_data_key = settings.STRIPE_DATA_KEY

    username = None

    if request.user.is_authenticated():
        username = request.user.id

    # check if there are any current orders against the user
    current_orders = Order.objects.filter(orderName=username, status__lt=4)

    return render(request, 'anotherapp/checkout.html', {'cart_items': cart_items, 'cart': cart_items,
                                                        'settings': db_settings, "nocart": True,
                                                        "stripe_data_key": stripe_data_key,
                                                        "current_orders": current_orders})


def final_checkout(request):
    # this function will charge the users card. This is the function called when the user pays for their products.

    if request.method == "POST":
        # Get all the contents in the cart, get the price and add it all together
        session = request.session['session_id']
        db_settings = Settings.objects.get(id=1)  # Get the delivery fee in the settings menu
        # Possibly delete above line of code and replace with an attribute inside the settings.py file
        tip = request.POST['form-tip']

        get_cart = Cart.objects.get(session=session)
        cart = CartItem.objects.filter(belongs_to_cart=get_cart).aggregate(Sum("total"))

        starter = float(
            cart['total__sum'])  # This variable contains the total number (without tax and delivery charge) as an Int
        price = (starter * float(db_settings.tax)) + starter  # Add the tax and the delivery charge
        print(starter)
        price += float(db_settings.deliveryFee)  # Delivery Charge

        if not tip:
            pass
        else:
            tip = float((request.POST['form-tip']))
            tip /= 100
            price += (price * tip)  # Add the tip to the bill that the user picked from the checkout page.
        price *= 100  # Turn the number into a stripe readable number (9.99 into 999.0)

        # Take any trailing digits after the decimal. It has already been multiplied by 100 to get rid of the cents.
        price = "%.0f" % price

        # Create the confirmation number:
        confirmation_number = uuid.uuid4().hex[:5].upper()

        import stripe
        # Set your secret key: ******* NOTE ******remember to change this to your live secret key in production
        # See your keys here https://dashboard.stripe.com/account/apikeys
        # Grab the stripe api key from the settings.py file
        stripe.api_key = settings.STRIPE_API_KEY

        # Get the credit card details submitted by the form
        token = request.POST['stripeToken']

        # Create the charge on Stripe's servers - this will charge the user's card
        try:
            charge = stripe.Charge.create(
                amount=price,  # amount in cents, again
                currency="usd",
                source=token,
                description="%s - %s - %s" % (session, request.user, confirmation_number)
            )
            user = request.user
            if not request.user.is_authenticated():
                user = None

            price = float(price)
            price /= 100

            query = Order(orderName=user, total=price, order_cart=get_cart, status=1, confirmation=confirmation_number)
            query.save()

            del request.session[
                'session_id']  # Delete the session but keep the carts variable. Ability to pull up the information later for re order
            return HttpResponseRedirect('/crm/dashboard/')

        except stripe.error.CardError as e:
            # The card has been declined
            pass


def successful_checkout(request):
    return render(request, 'anotherapp/success.html')


def order(request, confirmation):
    order_status = Order.objects.get(confirmation=confirmation)

    return render(request, "anotherapp/order.html", {"order": order_status})


def grab_cart_details(request, session_number):
    details = Cart.objects.filter(session_id=session_number)

    return render(request, "anotherapp/grab_cart_details.html", {"details": details})


def order_information(request):
    current_orders = Order.objects.filter(status__lt=4)

    return render(request, "anotherapp/information.html", {"current_orders": current_orders})


'''
########################################################################################

            Below here will contain all views for the store owner.

########################################################################################
'''


def store_owner_dashboard(request):
    current_orders = Order.objects.filter(status__lt=4).order_by("-id")

    if request.user.is_staff:
        return render(request, "anotherapp/owner.html", {"current_orders": current_orders, "nocart": True})
    else:
        raise Http404



def owner_engine(request):
    if request.method == "GET":
        method = request.GET.get('method', '')
        status = request.GET.get('status', '')
        if status == "Preparing":
            status = 1
        elif status == "Cooking":
            status = 2
        elif status == "Done":
            status = 3

        if method == "update-status":
            id = request.GET.get("id")
            order = Order.objects.get(id=id)
            order.status = status
            order.save()
    return HttpResponse('')
