from django.urls import path
from . import views

urlpatterns = [
    path('property_api_get',views.property_api_get,name='property_api_get'),
    path('property_api_get_by_id/<int:id>',views.property_api_get_by_id,name='property_api_get_by_id')
]

