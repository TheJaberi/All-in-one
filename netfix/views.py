from django.shortcuts import render, redirect
from datetime import timedelta

from users.models import User, Company, Customer
from services.models import Service, Request_service


def home(request):
    return render(request, 'users/home.html', {'user': request.user})


def customer_profile(request, name):
    try:
        # fetches the customer user and all of the services available by it
        user = User.objects.get(username=name)
        services = Request_service.objects.filter(
            customer=Customer.objects.get(user=user)).order_by("-date")
        # Calculate the new price for each service
        for service in services:
            price = service.service.price_hour
            hours = service.service_hours
            new_price = price * hours
            service.new_price = new_price
            service.date += timedelta(hours=3)
        return render(request, 'users/profile.html', {'user': user, 'services': services})
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