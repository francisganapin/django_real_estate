from django.shortcuts import render
from agent_page.models import Property
from django.db import connection
from django.shortcuts import get_object_or_404
from collections import defaultdict


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