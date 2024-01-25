

from django.urls import path, include
from .views import homepage, RealEstate, travel, vehicles, shopping, subscribe, website1

urlpatterns = [
    path('', homepage),
    path('realestate/', RealEstate),
    path('travel/', travel),
    path('vehicles/', vehicles),
    path('shopping/', shopping),
    path('listings/', website1),
    path('subscribe/', subscribe),
]
