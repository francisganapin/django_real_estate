from django.shortcuts import render
from agent_page.models import Property
from django.db import connection
from django.shortcuts import get_object_or_404

def front_page(request):
    
    return render(request,'user/index.html')

def contact_page(request):
    return render(request,'user/contact.html')

def property_page(request):
    return render(request,'user/properties.html')

def property_detail(request, id):
    property = get_object_or_404(
        Property.objects.prefetch_related(
            'features',
            'nearby_locations'
        ),
        id=id
    )
    print(property)
    return render(
        request,
        'user/property-detail.html',
        {'property': property}
    )