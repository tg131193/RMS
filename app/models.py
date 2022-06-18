from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from tinymce import models as tinymce_models
from tinymce.models import HTMLField


STATE_CHOICES = (
    ('Andaman & Nicobar Islands', 'Andaman & Nicobar Islands'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chandigarh', 'Chandigarh'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Dadra & Nagar Haveli', 'Dadra & Nagar Haveli'),
    ('Daman and Diu', 'Daman and Diu'),
    ('Delhi', 'Delhi'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu & Kashmir', 'Jammu & Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Puducherry', 'Puducherry'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttarakhand', 'Uttarakhand'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('West Bengal', 'West Bengal'),
)


class Customer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone=models.IntegerField()

    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)
    created=models.DateTimeField(auto_now_add=True)
    is_verify=models.BooleanField(default=False)
    is_updated=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return self.user.username
        return str(self.id)




CATEGORY_CHOICES = (
    
    ('V', 'veg'),
    ('NV', 'nonveg'),
    ('F', 'frozen Food'),
)


class Product(models.Model):
    title = models.CharField(max_length=100)

    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='media/producting')
    
    created=models.DateTimeField(auto_now_add=True)
    is_verify=models.BooleanField(default=False)
    is_updated=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(self.id)

        # Below Property will be used by checkout.html page to show total cost in order summary
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    @property
    def total(self):
        t=Cart.objects.all()
        amount=[]
        for l in t:

            amount=self.quantity * self.product.discounted_price
           
        shipping_amount = 0
        tempamount=amount

        if tempamount >= 1 and tempamount <= 200:
            shipping_amount = 20

        elif tempamount >= 201 and tempamount <= 500:
            shipping_amount = 30
        elif tempamount >= 501 and tempamount <= 999:
            shipping_amount = 40

        elif tempamount >= 1000 and tempamount <= 1500:
            shipping_amount = 50
        elif tempamount >= 1501 and tempamount <= 2000:
            shipping_amount = 55
        elif tempamount >= 2001 and tempamount <= 2500:
            shipping_amount = 60
        elif tempamount >= 2501:
            shipping_amount = 65


        return tempamount+shipping_amount
    @property   
    def shipping_ampunt(self):
        t=Cart.objects.all()
        amount=[]
        for l in t:

            amount=self.quantity * self.product.discounted_price
           
        shipping_amount = 0
        tempamount=amount

        if tempamount >= 1 and tempamount <= 200:
            shipping_amount = 20

        elif tempamount >= 201 and tempamount <= 500:
            shipping_amount = 30
        elif tempamount >= 501 and tempamount <= 999:
            shipping_amount = 40

        elif tempamount >= 1000 and tempamount <= 1500:
            shipping_amount = 50
        elif tempamount >= 1501 and tempamount <= 2000:
            shipping_amount = 55
        elif tempamount >= 2001 and tempamount <= 2500:
            shipping_amount = 60
        elif tempamount >= 2501:
            shipping_amount = 65


        return shipping_amount











STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel')
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    ordered_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='Pending')

     # Below Property will be used by orders.html page to show total cost
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

    @property
    def total_shipping(self):
        tempamount=0.0

        total = self.quantity * self.product.discounted_price
        tempamount +=total

        shipping_amount = 0.0

        if tempamount >= 1 and tempamount <= 200:
            shipping_amount = 20

        elif tempamount >= 201 and tempamount <= 500:
            shipping_amount = 30
        elif tempamount >= 501 and tempamount <= 999:
            shipping_amount = 40

        elif tempamount >= 1000 and tempamount <= 1500:
            shipping_amount = 50
        elif tempamount >= 1501 and tempamount <= 2000:
            shipping_amount = 55
        elif tempamount >= 2001 and tempamount <= 2500:
            shipping_amount = 60
        elif tempamount >= 2501:
            shipping_amount = 65

        return shipping_amount 
    @property
    def total_(self):

        total = self.quantity * self.product.discounted_price
        tempamount = total
        shipping_amount = 0

        if tempamount >= 1 and tempamount <= 200:
            shipping_amount = 20

        elif tempamount >= 201 and tempamount <= 500:
            shipping_amount = 30
        elif tempamount >= 501 and tempamount <= 999:
            shipping_amount = 40

        elif tempamount >= 1000 and tempamount <= 1500:
            shipping_amount = 50
        elif tempamount >= 1501 and tempamount <= 2000:
            shipping_amount = 55
        elif tempamount >= 2001 and tempamount <= 2500:
            shipping_amount = 60
        elif tempamount >= 2501:
            shipping_amount = 65

      

        return shipping_amount +self.quantity * self.product.discounted_price