from django.db import models
from django.utils import timezone

# Create your models here.

class AutoDateTimeField(models.DateTimeField): #stole this from stack  overlow, returns a time based on timezone. see line 14
    def pre_save(self, model_instance, add):
        return timezone.now()

class Customer(models.Model):
    name = models.CharField(max_length = 200, null = True)  #this defines the 'name' attribute of class Customer.  .Charfield is for a textfield input.
    phone = models.CharField(max_length = 200, null = True)
    email = models.CharField(max_length = 200, null = True)
    date_created = models.DateField(default=timezone.now, null = True)  #stole this from stackoverflow

    def __str__(self):
        return self.name   #returns the customer name in the admin page instead of bullshit

class Tag(models.Model):
    name = models.CharField(max_length= 200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
    ('Indoor', 'Indoor'),
    ('Outdoor', 'Outdoor'),
    ('Indoor/Outdoor', 'Indoor/Outdoor'),
    )   #this whole tuple get up is to make the choices used in the argument category  (choices = CATEGORY)
    name = models.CharField(max_length = 200, null = True)
    category = models.CharField(max_length = 200, null = True, choices = CATEGORY)
    description = models.CharField(max_length = 200, null = True)
    price = models.FloatField(max_length = 100000, null = True)  #this is a number/decimal input field to define the price attritube of class Product
    date_created = models.DateField(default=timezone.now, null = True) #stole from stackoverflow
    tag = models.ManyToManyField(Tag)   #creates a many to many relationship in the database with class Product using parent class Tag.


    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
    ('Pending', 'Pending'),
    ('Order Delivered', 'Order Delivered'),
    ('Delivered', 'Delivered'),
    )


    customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL) #creates a one to many relationship between customer in Order and the Customer class and all its attributes
    product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
    status = models.CharField(max_length = 200, null = True, choices = STATUS)
    date_created = models.DateField(default=timezone.now, null = True)
    note = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return (self.status + ' -- ' +  str(self.date_created))
