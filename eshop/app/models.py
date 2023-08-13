from django.contrib.auth.models import User
from django.db import models

# Create your models here.
CATEGORY_CHOISES = (
    ('PH', 'Phone'),
    ('TV', 'Television'),
    ('TA', 'Tablet'),
    ('PC', 'Personal computer'),
    ('WS', 'Watches')

)

STATE_CHOISES = (
    ('Czech Republic', 'Czech Republic'),
    ('Germany', 'Germany'),
    ('Austria', 'Austria'),
    ('Slovakia', 'Slovakia')
)


class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    discount = models.FloatField()
    description = models.CharField(max_length=1000)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOISES)
    image = models.ImageField(upload_to="product")

    def __str__(self):
        return self.title


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    state = models.CharField(choices=STATE_CHOISES, max_length=100)
    city = models.CharField(max_length=50)
    mobile_number = models.IntegerField(default=0)
    zip_code = models.IntegerField()

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.price


STATE_CHOISES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the way', 'On the way'),
    ('Delivered', 'Delivered'),
    ('Cancel ', 'Cancel'),
    ('Pending', 'Pending')
)


class Payment(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATE_CHOISES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")

    @property
    def total_cost(self):
        return self.quantity * self.product.discount


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.price

