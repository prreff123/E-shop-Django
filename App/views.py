from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponseRedirect
from .models import Product,Cateogry,Customer,Order
from django.views import View

# Create your views here.
class Login(View):
    return_url = None
    def get(self,request):
        Login.return_url = request.GET.get('return_url')
        return render(request,'login.html')
      
    def post(self,request):
        email = request.POST['email']
        password = request.POST['password']
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('index')
            else:
                error_message = 'Invalid Email or Password!!'    
        else:
            error_message = 'Invalid Email or Password!!'
        print(customer)
        print(email,password)
        return render(request,'login.html',{'error' : error_message})
        
def logout(request):
    request.session.clear()
    return redirect('login')

class OrderView(View):
    def get(self,request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request,'order.html',{'orders' : orders})

class Cart(View):
    def get(self,request):
        ids = (list(request.session.get('cart').keys()))
        products = Product.get_product_by_id(ids)
        print(products)
        return render(request,'cart.html',{'products' : products})

class CheckOut(View):
    def post(self,request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_product_by_id(list(cart.keys()))
        print(address,phone,customer,cart,products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id = customer),address=address,phone=phone,product=product,price=product.price,quantity=cart.get(str(product.id)))
            print(order.save())

            request.session['cart'] = {}    
        return redirect('cart')        

class Index(View):
    def post(self,request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1    
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print('cart',request.session['cart'])
        return redirect('index')

    def get(self,request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = None
        cateogries = Cateogry.get_all_cateogries()
        cateogryID = request.GET.get('cateogry')
        if cateogryID:
            products = Product.get_all_products_by_cateogryID(cateogryID)
        else:
            products = Product.get_all_products()
    
        data = {}
        data['products'] = products
        data['cateogries'] = cateogries
        print('You are : ',request.session.get('email'))
        # return render(request,'order.html')
        return render(request,'index.html',data)

def validatecustomer(new_custm):
    error_message = None
    if(not new_custm.first_name):
        error_message = "First Name Required!!"
    elif len(new_custm.first_name) < 4:
        error_message = "First Name must be 4 char long or more!"    

    elif(not new_custm.last_name):
        error_message = "Last Name Required!!"
    elif len(new_custm.last_name) < 4:
        error_message = "Last Name must be 4 char long or more!"    

    elif(not new_custm.phone):
        error_message = "Phone Number Required!!"
    elif len(new_custm.phone) < 10:
        error_message = "Phone must be 10 char long"    

    elif len(new_custm.password) < 5:
        error_message = "Password must be 5 char long!!"

    elif len(new_custm.email) < 5:
        error_message = "Email must be 5 char long"  

    elif new_custm.isExists():
        error_message = 'Email Address Already registerd...'    
    
    return error_message  

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        # validation
        value = {
            'first_name' : first_name,
            'last_name' : last_name,
            'phone' : phone,
            'email' : email
        }
        error_message = None
        
        new_custm =  Customer(first_name=first_name,last_name=last_name,email=email,password=password,phone=phone)
        error_message = validatecustomer(new_custm)
        
        if not error_message:
            print(first_name,last_name,phone,email,password)
            new_custm.password = make_password(new_custm.password)
            new_custm.save()
            return redirect('index')    

        else:
            data = {
                'error' : error_message,
                'values' : value
            }
            return render(request,'signup.html',data)    

    elif request.method == 'GET':
        return render(request,'signup.html')    
    
    else:
        return HttpResponseRedirect("An Acception Occured! Customer has been Added")       

def pay(request):
    
    return render(request, 'pay.html',)