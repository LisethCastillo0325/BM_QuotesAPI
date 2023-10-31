"""Contratos urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from django_api.quotes import views

router = DefaultRouter()
router.register(r'quotation', views.QuotationViewSet, basename='quotation')

urlpatterns = [
    path('', include(router.urls)),
]
