from django.shortcuts import render

from users.models import User, Company, Customer
from services.models import Service, Request_service


def home(request):
    return render(request, 'users/home.html', {'user': request.user})


def customer_profile(request, name):
    # fetches the customer user and all of the services available by it
    user = User.objects.get(username=name)
    services = Request_service.objects.filter(
        customer=Customer.objects.get(user=user)).order_by("-date")
    return render(request, 'users/profile.html', {'user': user, 'services': services})

def company_profile(request, name):
    # fetches the company user and all of the services available by it
    user = User.objects.get(username=name)
    services = Service.objects.filter(
        company=Company.objects.get(user=user)).order_by("-date")

    return render(request, 'users/profile.html', {'user': user, 'services': services})
