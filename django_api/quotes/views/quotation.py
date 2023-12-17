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
from django_api.utils.utils.utils import send_log_ekl

# Monitoring
from prometheus_client import Counter

# Métricas personalizadas
prometheus_c = Counter(
    'quotation_trafic', 'Number of request received in the Quotation API', ['method', 'endpoint'])

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..filter import QuotationViewFilter

# Models
from ..models.quotes import Quotation

# Serializers
from ..serializers import quotation as quotation_serializers

# Views
from django_api.utils.views.documents import DocumentsView


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
            return quotation_serializers.AddQuotationSerializer
        return quotation_serializers.QuotationModelSerializer

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request, *args, **kwargs):
        """ List quotes

            Allows listing all invoices registered in the system.
        """
        prometheus_c.labels('get', 'quotation/').inc()
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ Query quotation by ID

            Allows obtaining information about an quotation given its ID.
        """  
        prometheus_c.labels('get', 'quotation/<id>').inc()
        return super().retrieve(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """ Create a quotation

            Create quotation
        """
        prometheus_c.labels('post', 'quotation/').inc()
        serializer = quotation_serializers.AddQuotationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Create an invoice for the quotation
        quotation = serializer.save()
        
        data = quotation_serializers.QuotationModelSerializer(instance=quotation).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """ Deactivate quotation

            Allows canceling an quotation, does not delete it.
        """
        prometheus_c.labels('delete', 'quotation/').inc()
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        """Method invoked by 'destroy' to change the state of the Quotation."""
        instance.is_active = False
        instance.save()

    @action(detail=True, methods=['GET'])
    def download(self, request, *args, **kwargs):
        """ Download quotation PDF

            Given an quotation ID, allows downloading its PDF representation.
        """
        prometheus_c.labels('get', 'quotation/download/').inc()
        instance = self.get_object()
        send_log_ekl("Descarga de cotización #{}".format(instance.id))
        data = self.get_serializer(instance=instance).data

        # Query current advertising
        data['api_url'] = settings.URL_BACKEND
        template = os.path.join('documents', 'invoice.html')
        documents_view = DocumentsView()

        try:
            return documents_view.generate_pdf(
                template=template,
                data=data,
                file_name='invoice_{}_{}'.format(instance.id, instance.client)
            )
        except Exception as error:
            send_log_ekl("Error presentado en {}: {}".format(self.__class__.__name__, str(error)))
            raise error
