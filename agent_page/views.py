from django.shortcuts import render
from django.db import connection
# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Property




@api_view(['GET'])
def property_api_get(request):



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

