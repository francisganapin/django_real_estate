from django.shortcuts import render
from django.db import connection
# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Property,PropertyViews,PropertyInquiry

from django.core.paginator import Paginator
from django.shortcuts import render
from better_profanity import profanity


from django.db.models import Count

@api_view(['GET'])
def property_api_get_clean(request):
    page = int(request.GET.get('page',1))
    page_size = int(request.GET.get('page_size',6))
    offset = (page - 1) * page_size

    #Get Filter Parameters
    property_type = request.GET.get('property_type','')
    status_filter = request.GET.get('status','')
    min_price = request.GET.get('min_price','')
    max_price = request.GET.get('max_price','')

    conditions = []
    params = []

    conditions.append('is_active = 1')

    if property_type:
        conditions.append('property_type = %s')
        params.append(property_type)

    if status_filter:
        conditions.append('status = %s')
        params.append(status_filter)

    if min_price:
        conditions.append('price >= %s')
        params.append(min_price)

    if max_price:
        conditions.append('price <= %s')
        params.append(max_price)


    where_clause = ""
    if conditions:
        where_clause = 'WHERE ' + ' AND '.join(conditions)   



    with connection.cursor() as cursor:
        cursor.execute(f"SELECT count(*) FROM agent_page_property {where_clause}",params)

        columns = [col[0] for col in cursor.description]
        total_count = cursor.fetchone()[0]

        cursor.execute(f"""
            SELECT id,title,price,bathrooms,bedrooms,
            square_feet,city,state,
            main_image,
            status FROM agent_page_property

            {where_clause}
            ORDER BY id DESC
            LIMIT %s
            OFFSET %s
        """,params + [page_size,offset])
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        

    results = [dict(zip(columns, row)) for row in rows]
    
    return Response({
        'count':total_count,
        'total_pages':(total_count + page_size - 1) // page_size,
        'current_page':page,
        'page_size': page_size,
        'next': f'?page={page + 1}' if offset + page_size < total_count else None,
        'previous': f'?page={page - 1}' if page > 1 else None,
        'results':results   
        })










@api_view(['GET'])
def property_api_get_by_id(request, id):
    try:
        property = Property.objects.prefetch_related(
            "features",
            "nearby_locations"
        ).get(id=id)
    except Property.DoesNotExist:
        return Response(
            {"detail": "Property not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response({
        "id": property.id,
        "title": property.title,
        "price": property.price,
        "property_type": property.property_type,
        "status": property.status,
        "bedrooms": property.bedrooms,
        "bathrooms": property.bathrooms,
        "square_feet": property.square_feet,
        "description": property.description,
        "address": property.address,
        "city": property.city,
        "state": property.state,
        "zip_code": property.zip_code,  
        "views":0,
        "date_added":property.created_at,
        "features": [
            {
                "name": f.name,
                "description": f.description
            }
            for f in property.features.all()
        ],
        "nearby_locations": [
            {
                "name": n.name,
                "location_type": n.location_type,
                "distance": n.distance,
                "distance_unit": n.distance_unit
            }
            for n in property.nearby_locations.all()
        ]
    })


@api_view(['PUT'])
def update_property(request, id):
    try:
        property = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return Response({"detail": "Property not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    
    # Update fields if present in request data
    if 'title' in data: property.title = data['title']
    if 'property_type' in data: property.property_type = data['property_type']
    if 'status' in data: property.status = data['status']
    if 'price' in data: property.price = data['price']
    if 'bedrooms' in data: property.bedrooms = data['bedrooms']
    if 'bathrooms' in data: property.bathrooms = data['bathrooms']
    if 'square_feet' in data: property.square_feet = data['square_feet']
    if 'description' in data: property.description = data['description']
    if 'address' in data: property.address = data['address']
    # You can add more fields as needed

    try:
        property.save()
        return Response({"detail": "Property updated successfully"})
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def approve_property(request,id):
    try:
        property = Property.objects.get(id=id)
        property.is_active = True
        property.save()
        return Response({"detail": "Property approved successfully"})
    except Property.DoesNotExist:
        return Response({"detail": "Property not found"}, status=status.HTTP_404_NOT_FOUND)



def dashboard_page(request):
    properties = Property.objects.all()
    count = len(properties)
    count_active = len(properties.filter(is_active=True))
    count_views = len(PropertyViews.objects.all())
    count_message = len(PropertyInquiry.objects.all())

    return render(request,'admin/dashboard.html',{'properties':properties[:5],'count':count,
    'count_active':count_active,'count_views':count_views,
    'count_message':count_message
    
    })



def message_page(request):
    messages = PropertyInquiry.objects.all()
    return render(request,'admin/messages.html',{'messages':messages})


def property_admin_page(request):
    properties = Property.objects.filter(is_active=True).annotate(
    view_count =Count('views'))

    status = request.GET.get('status')
    property_type = request.GET.get('property_type')

    if status and status != 'All Status':
        properties = properties.filter(status=status)

    if property_type and property_type != 'All Types':
        properties = properties.filter(property_type=property_type)


    paginator = Paginator(properties,8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'admin/properties.html',{'page_obj':page_obj})



def property_admin_pre_dirty_page(request):
    properties = Property.objects.filter(is_active=False)
    paginator = Paginator(properties,8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'admin/dirty_properties.html',{'page_obj':page_obj})

