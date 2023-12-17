from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Monitoring
from prometheus_client import generate_latest, REGISTRY


class MonitoringViewSet(viewsets.GenericViewSet):

    @action(detail=False, methods=['GET'])
    def traffic_monitoring(self, request, **kwargs):
        try:
            # Obtener métricas
            metrics = generate_latest(REGISTRY)
            return HttpResponse(metrics, content_type='text/plain; version=0.0.4')
        except Exception as e:
            print('Error al obtener métricas:', e)
            return Response('Error al obtener métricas', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
