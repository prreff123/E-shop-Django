from django.contrib import admin
from .models import Product,Cateogry,Customer,Order

# Register your models here.

class AdminProduct(admin.ModelAdmin):
    list_display = ['name','price','cateogry']

admin.site.register(Product,AdminProduct)
admin.site.register(Cateogry)
admin.site.register(Customer)
admin.site.register(Order)
