from django.contrib.auth.forms import UserCreationForm   #since we dont fuck with all the models and shit database side with the usercreation django gives us,  if we want to customize this form we need to import it from the django files
from django.forms import ModelForm      #used to make a form based off of a model the django way
from django import forms

#our models that we'll be calling on to create forms
from .models import Order, Customer
from django.contrib.auth.models import User             # see above, we also need a model for our meta for usercreate. in this case it already exists in django. they make it so easy. so we just import it. this comes from the docs



class OrderForm(ModelForm):  #this is how you create a form in django for use in views.  use ModelForm as an argument as per the docs
    class Meta:             #this meta class refers to the model that you want to make a form from. you're going to be entering objects referring to th emodel. see docs
        model = Order           #define which model you're using
        fields = '__all__'      #define which fields from the model you're using. in this case all.

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class CreateUserForm(UserCreationForm):                 #we're creating a custom usercreation form based off of the django UserCreationForm. same process as above
    class Meta:
        model = User
        fields = ['username','email', 'password1','password2']
