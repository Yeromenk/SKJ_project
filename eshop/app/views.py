import razorpay
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View

from .forms import CustomerRegistrationForm, CustomerAccountForm
from .models import Payment
from .models import Product, Customer, Cart, OrderPlaced, Wishlist


# Create your views here.
def home(request):
    return render(request, "app/mainpage.html")


def about(request):
    return render(request, "app/about.html")


class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html", locals())


class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, "app/category.html", locals())


class DetailProduct(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product))
        return render(request, "app/detailproduct.html", locals())


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "app/customerregistration.html", locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User registered successfully!")
        else:
            messages.warning(request, "Invalid input data")
        return render(request, 'app/customerregistration.html', locals())


class ProfileView(View):
    def get(self, request):
        form = CustomerAccountForm()
        return render(request, 'app/profile.html', locals())

    def post(self, request):
        form = CustomerAccountForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            # locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile_number = form.cleaned_data['mobile_number']
            state = form.cleaned_data['state']
            zip_code = form.cleaned_data['zip_code']

            reg = Customer(user=user, name=name, mobile_number=mobile_number, city=city, state=state,
                           zip_code=zip_code)
            reg.save()
            messages.success(request, "Profile saved successfully!")
        else:
            messages.warning(request, "Some problems")
        return render(request, 'app/profile.html', locals())


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discount
        amount = amount + value
    total_amount = amount + 40
    return render(request, 'app/add_to_cart.html', locals())


class checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discount
            famount = famount + value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency": "CZK", "receipt": "order_rcptid_22"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()
        return render(request, 'app/checkout.html', locals())


def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', locals())


def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user = request.user
    customer = Customer.objects.get(id=cust_id)

    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
        c.delete()
    return redirect("orders")


def search(request):
    query = request.GET['search']
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, "app/search.html", locals())


def new_wishlist(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Wishlist(user=user, product=product).save()
    return redirect("/wishlist")


def show_wishlist(request):
    user = request.user
    wishlist = Wishlist.objects.filter(user=user)
    return render(request, 'app/wishlist.html', locals())
