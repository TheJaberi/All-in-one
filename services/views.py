from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from users.models import Company, Customer, User

from .models import Service
from .forms import CreateNewService, RequestServiceForm


def service_list(request):
    services = Service.objects.all().order_by("-date")
    return render(request, 'services/list.html', {'services': services})


def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})


def create(request):
    if not request.user.is_company:
        return redirect('/')
    if request.method == 'POST':
        # print(f'hello request "{request.POST}"')
        form = CreateNewService(request.POST)
        if form.is_valid():
            title = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price_hour = form.cleaned_data['price_hour']
            field = form.cleaned_data['field']
            company = Company.objects.get(user=request.user)
            Service.objects.create(
                name=title, description=description, price_hour=price_hour, field=field, company=company)
            return HttpResponseRedirect('/services/')
        elif form.errors:
            return render(request, 'services/create.html', {'form': form})
    else:
        form = CreateNewService()
        return render(request, 'services/create.html', {'form': form})


def service_field(request, field):
    # search for the service present in the url
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(
        field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})


def request_service(request, id):
    return render(request, 'services/request_service.html', {})
