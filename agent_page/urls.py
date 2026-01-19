from django.urls import path
from . import views

urlpatterns = [
    path('property_api_get',views.property_api_get,name='property_api_get'),
    path('property_api_get_by_id/<int:id>',views.property_api_get_by_id,name='property_api_get_by_id'),


    path('dashboard_page/',views.dashboard_page,name='dashboard_page'),
    path('message_page/',views.message_page,name='message_page'),
    path('property_admin_page/',views.property_admin_page,name='property_admin_page')

]

