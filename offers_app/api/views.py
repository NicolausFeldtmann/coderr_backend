from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from offers_app.models import OfferModel, OfferDetails
from .serializers import OfferSerializer, OfferListSerializer, DetailSerializer, OfferRetriveSerializer
from .permissions import IsOwnerOrAdmin, IsOfferAuthorOrAdmin
from .paginations import CustomResultSetPagination
from .filters import CustomOfferFilter

class OfferListView(generics.ListCreateAPIView):
    """ View to handle GET and POST requests for offer list. """

    queryset = OfferModel.objects.prefetch_related("details").distinct().order_by('id')
    permission_classes = [IsOfferAuthorOrAdmin]
    pagination_class = CustomResultSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CustomOfferFilter
    search_fields = ['title', 'description', 'user__username']

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OfferListSerializer
        return OfferSerializer

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_serializer = OfferSerializer(serializer.instance)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ View to handle GET, PATCH and DELETE requests for single offers. """

    queryset = OfferModel.objects.prefetch_related("details").all()
    permission_classes = [IsOfferAuthorOrAdmin, IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return OfferRetriveSerializer
        return OfferSerializer

class OfferDetailsRetrieveView(generics.RetrieveAPIView):
    """ View to handle GET requests for single offer details. """

    queryset = OfferDetails.objects.all()
    serializer_class = DetailSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'price', 'delivery_time', 'offer_type']


    