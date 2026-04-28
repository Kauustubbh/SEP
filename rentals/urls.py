from django.urls import path
from . import views

urlpatterns = [
    path('rent/<int:item_id>/', views.rental_request_view, name='rental_request'),
    path('rental/<int:rental_id>/approve/', views.rental_approve_view, name='rental_approve'),
    path('rental/<int:rental_id>/reject/', views.rental_reject_view, name='rental_reject'),
    path('rental/<int:rental_id>/complete/', views.rental_complete_view, name='rental_complete'),
]
