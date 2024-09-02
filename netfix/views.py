from django.shortcuts import render, redirect
from datetime import timedelta, datetime

from users.models import User, Company, Customer
from services.models import Service, Request_service


def home(request):
    return render(request, 'users/home.html', {'user': request.user})


def customer_profile(request, name):
    try:
        # fetches the customer user and all of the services available by it
        user = User.objects.get(username=name)
        if user.is_company:
            return redirect('/')
        services = Request_service.objects.filter(
            customer=Customer.objects.get(user=user)).order_by("-date")
        # Calculate the new price for each service
        for service in services:
            price = service.service.price_hour
            hours = service.service_hours
            new_price = price * hours
            service.new_price = new_price
            service.date += timedelta(hours=3)
        
                
        age = 0
        if user.is_customer:
            birth_date = Customer.objects.get(user=user).birth
            current_date = datetime.today()
            age = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))
        
        if age < 0:
            age = "You are not born yet"
        else:
            age = "You are " + str(age) + " years old"
            
        return render(request, 'users/profile.html', {'user': user, 'services': services, 'age': age})
    except User.DoesNotExist:
        return redirect('/')

def company_profile(request, name):
    try:
        # fetches the company user and all of the services available by it
        user = User.objects.get(username=name)
        services = Service.objects.filter(
            company=Company.objects.get(user=user)).order_by("-date")

        return render(request, 'users/profile.html', {'user': user, 'services': services})
    except Exception:
        return redirect('/')