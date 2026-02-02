from django.shortcuts import render
from agent_page.models import Property, PropertyViews
from django.db import connection
from django.shortcuts import get_object_or_404
from collections import defaultdict

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def front_page(request):
    return render(request,'user/index.html')

def contact_page(request):
    return render(request,'user/contact.html')

def property_page(request):
    return render(request,'user/properties.html')

def admin_login(request):
    return render(request,'user/admin_login.html')

def property_detail(request, id):
    property = get_object_or_404(
        Property.objects.prefetch_related(
            'features',
            'nearby_locations'
        ),
        id=id
    )
    
    # Track View
    ip = get_client_ip(request)
    PropertyViews.objects.create(property=property, ip_address=ip)
    
    nearby_locations = property.nearby_locations.all()

    grouped_locations = defaultdict(list)

    for loc in nearby_locations:
        grouped_locations[loc.get_location_type_display()].append(loc)

    return render(
        request,
        'user/property-detail.html',
        {
            'property': property,
            'grouped_locations': dict(grouped_locations)  # Convert to regular dict for template
        }
    )