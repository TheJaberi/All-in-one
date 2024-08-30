from django.urls import path
from django.contrib.auth import views

from .forms import UserLoginForm
from . import views as v

urlpatterns = [
    path('customer/', v.Customer_signup_view, name='customer_signup'),
    path('company/', v.Company_signup_view, name='company_signup'),
    path('', v.Login_view, name='login'),
    path('new/', v.register, name='new')
]
