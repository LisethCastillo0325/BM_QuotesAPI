import os
from django.utils import timezone
from django.conf import settings
from django.db import transaction

# Rest Framework
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..filter import QuotationViewFilter

# Models
from ..models.quotes import Quotation

# Serializers
from ..serializers import quotation as quotation_serialisers

# Views
from django_api.utils.views.documentos import DocumentosView

# Service
from django_api.quotes.services.quotation import QuotationServices


class QuotationViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):

    queryset = Quotation.objects.all()
    # permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['client']
    ordering_fields = ['id']
    filterset_class = QuotationViewFilter

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == 'create':
            return quotation_serialisers.AddQuotationSerializer
        return quotation_serialisers.QuotationModelSerializer

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request, *args, **kwargs):
        """ Listar facturas

            Permite listar todos los facturas registradas en el sistema.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ Consultar factura por ID

            Permite obtener información de un factura dado su ID
        """  
        return super().retrieve(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """ Crear factura para un quotation

            Dado un quotation se crea su factura respectiva.
        """
        serializer = quotation_serialisers.AddQuotationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Crear factura al quotation
        quotation = serializer.save()
        
        data = quotation_serialisers.QuotationModelSerializer(instance=quotation).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """ Inactivar factura

            Permite anular una factura, no lo elimina.
        """
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        """Metodo invocado por 'destroy' para cambiar el estado del Quotation."""
        instance.is_active = False
        instance.save()

    @action(detail=True, methods=['GET'])
    def descargar(self, request, *args, **kwargs):
        """ Descargar Factura PDF

            Dado un ID de factura permite descargar su representación en PDF.
        """

        instance = self.get_object()
        data = self.get_serializer(instance=instance).data

        # Consultar publicidad vigente
        data['url_api'] = settings.URL_BACKEND

        template = os.path.join('documentos', 'factura.html')
        documentos_view = DocumentosView()

        return documentos_view.generar_pdf(
            template=template,
            data=data,
            file_name='factura_{}_{}'.format(instance.id, instance.client)
        )
        