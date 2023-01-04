from django.db import models
import datetime

# Create your models 
class Cateogry(models.Model):
    name = models.CharField(max_length=20)

    @staticmethod
    def get_all_cateogries():
        return Cateogry.objects.all()

    def __str__(self):
        return self.name
        
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    cateogry = models.ForeignKey(Cateogry, on_delete=models.CASCADE,default=1)
    description = models.CharField(max_length=200,default='',)
    image = models.ImageField(upload_to = 'products/')

    @staticmethod
    def get_product_by_id(ids):
        return Product.objects.filter(id__in = ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()
    
    @staticmethod
    def get_all_products_by_cateogryID(cateogry_id):
        if cateogry_id:
            return Product.objects.filter(cateogry = cateogry_id)
        else:
            return Product.get_all_products()    

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=20)

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email = email)
        except:
            return False
              
    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True    
        return False        

class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50,default='',blank=True)
    phone = models.CharField(max_length=10,default='')
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def placeorder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer = customer_id).order_by('-date')