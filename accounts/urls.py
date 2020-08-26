#from django.contrib.auth import views as auth_views   #some weird shit to make the login requried decorator work


from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('admin/', admin.site.urls, name='admin'),
    path('', views.home, name='home'),
    path('customer/<str:pk>/', views.customer, name='customer'),
    path('products/', views.products, name='products'),
    path('createorder/<str:pk>/', views.createorder, name='createorder'),
    path('deleteorder/<str:pk>/', views.deleteorder, name='deleteorder' ),
    path('updateorder/<str:pk>/', views.updateorder, name='updateorder' ),
    path('updatecustomer/<str:pk>/', views.updatecustomer, name='updatecustomer'),
    path('createcustomer', views.createcustomer, name='createcustomer'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.register, name='register'),
    #path('accounts/login/', auth_views.LoginView.as_view())           #makes the login_required ecorator redirect to login page

]
