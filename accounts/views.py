from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import  inlineformset_factory
from django.contrib.auth.forms import UserCreationForm     #premade django form for user create, for a login page, super handy
from django.contrib import messages                 #allows you to customize messages, we're customizing the django error messages. see docs for other messages you can fiddle with
from django.contrib.auth import authenticate, login, logout        #built in authenticate, login, logout functions from django, super tight
from django.contrib.auth.decorators import login_required

from accounts.filters import OrderFilter
from accounts.models import *
from accounts.forms import OrderForm, CustomerForm, CreateUserForm
from accounts.decorators import authenticated_usercheck, allowed_users

# Create your views here.

@authenticated_usercheck                                #custom decorator, check out decorators.py then check the docs
def loginPage(request):
    if request.method == 'POST':                        #refers to the form action of login page html. line 86
        username= request.POST.get('username')        #queries from the input of login page form. line 91 login.html
        password= request.POST.get('password')        #queries from the input of login page form. line 97 login.html
        user = authenticate(request, username=username, password=password)             #straight from authenticate docs. takes those 3 arguments. string values of username and password are whatever you defined from the queryset above
        if user is not None:                           #seems strange, but actually says "if the user is authenticated" aka has a value, aka not a value of None
            login(request, user)                    #this automatically logs in something. that something is defined by the request, and "something". in this case "Something" is our user from the authenticate query above.
            return redirect('/')                    #we know what this is
        else: messages.info(request, 'Username or Password is Incorrect')               # do this thing and throw it into the tmeplate

    context = {}
    #bring in user validate form
    #save user validate form
    #redirect to home
    return render(request, 'accounts/login.html', context)


def logoutUser(request):                    #simple logout
    logout(request)                         #imported function above from django. all it takes is a request as an argument. go to navbar.html lines 14-19 to see how to implement this view as a link. make sure you have the url path set up in urls.py
    return redirect('/login')                #once theyve logged out, redirect to them to login page

@authenticated_usercheck
def register(request):
    #form = UserCreationForm()                      #bring in a user creation form, this is why we imported that dope django premade usercreate form above
    form = CreateUserForm()                             ##custom based in forms.py, always import!
    if request.method == 'POST':
        #form = UserCreationForm(request.POST)      #pass in the stuff entered into the form, into the django UserCreationForm method.
        form = CreateUserForm(request.POST)             ##custom
        if form.is_valid():
            form.save()                             #.save() user recreation form
            user = form.cleaned_data.get('username')            #once a form.is_valid() you can call on it's data as a string with the .cleaned_data.get(nameofformfield)
            messages.success(request, 'Account was created')            #after importing messages from django.contrib, this is how you make a custom message.  do this command. then throw it into the html template you want to render the message in
            return render(request, 'accounts/login.html')
        else:
            messages.warning(request, 'Account unable to be created. Make sure all the fields are accurate.')           #it turns out this messages shit only works if theres an else statement. dont know why, but throw one in there even if its useless

    context = {
    'form': form,
    }


    #.redirect to login page
    return render(request, 'accounts/register.html', context)

@login_required(login_url='/login')                 #this is a decorator. we imported it above. stick it above a view. this one makes it so you can only access the view if you're logged in, if not, rederiects you to login page. setting login_url to where you wanna redirect, probably a llgin login page. straight from django
@allowed_users(allowed_roles=['employee'])          #custom decorator built in decorats.py and imported above
def home(request):
    orders = Order.objects.all()                    #1.make the query from models ( Order.objects.all() ) , 2.put it into an attribute (orders), 3. pass attribute into context. see below
    customers = Customer.objects.all()              #do the same for any data you want from you models to use dynamically on your site... make sure to includ the {{contextname}} or {%%} tags in your html
    total_customers = customers.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    total_orders = orders.count()

    context = {
    'orders': orders, 'customers': customers,
    'total_customers': total_customers, 'delivered': delivered, 'pending': pending, 'total_orders': total_orders,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='/login')
def products(request):
    products = Product.objects.all()
    context = {
    'products': products,
    }
    return render(request, 'accounts/products.html', context)



@login_required(login_url='/login')
def customer(request, pk):                  #pk, or primary key, is an argument you can pass through a view for a specific instance.  in our case we want the instance of a specific customer
    customer = Customer.objects.get(id=pk)      #this the queryset command to pull the id of a customer
    orders = customer.order_set.all()           #this is a queryset to get the orderset of customer. its for a form, see below
    total_orders = orders.count()

    orderFilter = OrderFilter(request.GET, queryset= orders)     #this is for django-filter, look up docs.  our query set is an argument this djang-filter thing takes to specify which data i.e. this specific customer's orders as defined in orders above
    orders = orderFilter.qs                           #this is the lynchpin of how the search takes place database side. we've built the variable orders above, then filtered it with our filter, and now are being served back this filtered version of orders via render(context) below

    context = {
    'customer': customer,
    'orders': orders,
    'total_orders': total_orders,
    'orderFilter': orderFilter,
    }
    return render(request, 'accounts/customer.html', context)



@login_required(login_url='/login')
def createorder(request, pk):
    customer = Customer.objects.get(id=pk)                          #get specific customer, then pass id into argument as pk
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status',), extra=5)               #choose your models in models.py you want in your formset. then the fields from the objects of the models. extra is how many of the formsets you want
    #form = OrderForm(initial= {'customer': customer})  #use the specific customer as defined in the previous line as the customer object from the Order class
    formset = OrderFormSet(queryset=Order.objects.none() ,instance=customer)      #to pass a specific customer into the OrderFormset, do instance= to the customer or item you attrivuted above.  queryset is another argument to pass into OrderFormset. it tell which, if any, objects to query from the model. in this case we use a command for none.
    if request.method == 'POST':            #this is the straight up copy pasted loop to save an item to the database tied to the method of an html tag in your template
        #form = OrderForm(request.POST)
        formset =  OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')   #returns to main url

    context = {
    'formset': formset,                                     #always pass your context
    'customer': customer,
    }
    return render(request, 'accounts/orderform.html', context)



@login_required(login_url='/login')
def deleteorder(request, pk):
    order = Order.objects.get(id=pk)   #gets and order with a specific id from the Order class.  the id is given value pk to return to the function as an argument.
    form = OrderForm(instance = order)

    if request.method == 'POST':           #same save function as above refers to the method in the html form tag.
        order.delete()       #the delete function for an item in our database. in this case, the one with tthe specific one from above.
        return redirect('/')

    context = {
    'order': order,
    'form': form,
    }
    return render(request, 'accounts/deleteorderform.html', context)




@login_required(login_url='/login')
def updateorder(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance = order)      #prefills the form with the stuff to the specific order id

    if request.method == 'POST':           #same save function as above
        form = OrderForm(request.POST, instance= order)  #again saves that specific instance instead of making a new one.
        if form.is_valid():
            form.save()
            return redirect('/')

    context={
    'form': form,
    }
    return render(request, 'accounts/updateorderform.html', context)




@login_required(login_url='/login')
def orderform(request):
    return render(request, 'accounts/orderform.html')




@login_required(login_url='/login')
def updatecustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance = customer)
    if request.method == 'POST':           #same save function as above
        form = CustomerForm(request.POST, instance= customer)  #again saves that specific instance instead of making a new one.
        if form.is_valid():
            form.save()
            return redirect('/')


    context = {
    'form': form,
    'customer': customer
    }

    return render(request, 'accounts/customerform.html', context)




@login_required(login_url='/login')
def createcustomer(request):
    form = CustomerForm()
    if request.method == 'POST':           #same save function as above
        form = CustomerForm(request.POST)  #again saves that specific instance instead of making a new one.
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
    'form': form,
    }
    return render(request, 'accounts/customerform.html', context)
