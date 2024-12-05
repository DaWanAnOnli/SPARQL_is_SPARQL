from django.urls import path
from .views import results_view, airport_view, country_view, navaid_view, region_view, runway_view, all_airports, all_countries


urlpatterns = [
    path('', results_view, name='results_view'),
    path('airports/<str:airport_id>/', airport_view, name='airport_details'),
    path('countries/<str:iso_country>/', country_view, name='country_details'),
    path('navaids/<str:navaid_id>/', navaid_view, name='navaid_details'),
    path('regions/<str:region_id>/', region_view, name='region_details'),
    path('runways/<str:runway_id>/', runway_view, name='runway_details'),


    path('airports/', all_airports, name='all_airports'),
    path('countries/', all_countries, name='all_countries'),
]
