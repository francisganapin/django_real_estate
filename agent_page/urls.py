from django.urls import path
from . import views


urlpatterns = [
    #this data was dirty
    path('property_admin_pre_dirty_page/',views.property_admin_pre_dirty_page,name='property_admin_pre_dirty_page'),
    #this data will show only on front page
    path('property_api_get_clean',views.property_api_get_clean,name='property_api_get_clean'),
    #this data was clean

    path('property_api_get_by_id/<int:id>',views.property_api_get_by_id,name='property_api_get_by_id'),


    path('dashboard_page/',views.dashboard_page,name='dashboard_page'),
    path('message_page/',views.message_page,name='message_page'),
    path('property_admin_page/',views.property_admin_page,name='property_admin_page'),
    path('update_property/<int:id>',views.update_property,name='update_property'),



    path('approve_property/<int:id>',views.approve_property,name='approve_property')
]

