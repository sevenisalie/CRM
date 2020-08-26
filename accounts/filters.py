import django_filters
from django_filters import DateFilter, CharFilter     #check out docs for this at django-filters
from accounts.models import *

class OrderFilter(django_filters.FilterSet):      #just like forms.py. always put in django_filters.FilterSet as per the docs
    start_date = DateFilter(field_name="date_created", lookup_expr="gte")  #this is our first custom attribute.  we're using the imported DateFilter function and this function requires an argument of field.  field refers to the attribute of the class in models.py you're basing the custom attribut eoff of
    end_date = DateFilter(field_name="date_created", lookup_expr="lte")  #it also takes argument lookup_expr which we are using greaterthan or equal to and vice versa to do a start and end date for the orders
    note = CharFilter(field_name="note", lookup_expr="icontains")       #using CharFilter, same as above, but this lookup expr is shorthand for icontains means ignore case sensitiviy for all text in CharFilter
    class Meta:
        model = Order            #this meta attribute refers to which class in models.py you're making a filter of
        fields = '__all__'         #this is how you have it return all fields from the model you specified
        exclude = 'customer', 'date_created'                #this is how you exclude certain fields from the model you specified from showing up. make sure its after the __all__
