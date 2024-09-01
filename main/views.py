from django.shortcuts import render
from django.contrib.auth import logout as django_logout

from django.db.models import Count
from services.models import Request_service, Service

def home(request):
    # get top 5 most requested services
    top_5_services_names = list(
        Request_service.objects
        .values_list('service__name', flat=True)
        .annotate(count=Count('service'))
        .order_by('-count')[:5]
    )

    # Query services
    top_5_services = list(Service.objects.filter(name__in=top_5_services_names))

    # Create a mapping from service name to its position
    name_to_position = {name: index for index, name in enumerate(top_5_services_names)}

    # Sort the list based on the position
    top_5_services.sort(key=lambda s: name_to_position[s.name])

    if request.user.is_authenticated:
        return render(request, "main/home.html", {"user": request.user, "top_5_services": top_5_services})
    else :
        return render(request, "main/home.html", {"top_5_services": top_5_services})


def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")
