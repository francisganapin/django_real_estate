from django.urls import path
from . import views

urlpatterns = [
    path('',views.front_page,name='front_page'),
    path('properties/',views.property_page,name='property_page'),
    path('admin_login/',views.admin_login,name='admin_login'),


    #this one we get the id of our views on via url
    path('property/<int:id>/',views.property_detail,name='property_detail'),
    path('contact/',views.contact_page,name='contact_page'),
]

