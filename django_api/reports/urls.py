"""Users urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from django_api.reports import views

router = DefaultRouter()
router.register(r'report/clients', views.ClientReportsViewSet, basename='report_clients')
router.register(r'report/monitoring', views.MonitoringViewSet, basename='report_monitoring')

urlpatterns = [
    path('', include(router.urls)),
]
