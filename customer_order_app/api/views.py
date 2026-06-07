from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import BasePagination
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from customer_order_app.models import OrderModel
from .serializers import OrderSerializer, CreateOrderSerializer, UpdateSerializer
from .permissions import IsOrderOwner, IsCustomer

class NoPagination(BasePagination):
    """ Deactivates paginations """

    def paginate_queryset(self, queryset, request, view=None):
        """ Cancels all pagination intructions. Returns all results in one list """
        return list(queryset)

    def get_paginated_response(self, data):
        """ Returns all results without pagintation-wrapper. """
        return Response(data)

class OrderViewSet(viewsets.ModelViewSet):
    """ View that handles incommig POST or GET requests for orders. """
    
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = NoPagination

    def get_permissions(self):
        """ Method to set different permissions based on request method. """

        if self.request.method == "POST":
            return [IsAuthenticated(), IsCustomer()]
        elif self.request.method == "PATCH":
            return [IsAuthenticated(), IsOrderOwner()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        """ Selects serializers for different operations. """
        if self.action == "create":
            return CreateOrderSerializer
        elif self.action == "partial_update":
            return UpdateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        """ Function to create new order entry. """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        output_serializer = OrderSerializer(order)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        """ Function to patch existing order and return full data. """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        output_serializer = OrderSerializer(order)
        return Response(output_serializer.data)

class OrderCountView(generics.GenericAPIView):
    """ View for GET requests to list all orders excepting completed orders. """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """ Retrives the sum of all orders of business-user. """
        business_user_id = self.kwargs.get('business_user_id')
        get_object_or_404(User, id=business_user_id)

        order_count = OrderModel.objects.filter(
            business_user_id=business_user_id,
            status__in=['pending', 'in_progress']
        ).count()

        return Response({'order_count': order_count})

class OrderCountCompletedView(generics.GenericAPIView):
    """ View for GET requests to list all status compoleted orders. """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """ Retrieves the sum of all completed-orders. """
        business_user_id = self.kwargs.get('business_user_id')
        get_object_or_404(User, id=business_user_id)

        order_count = OrderModel.objects.filter(
            business_user_id=business_user_id,
            status__in=['completed']
        ).count()

        return Response({"completed_order_count": order_count})