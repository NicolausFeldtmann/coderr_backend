from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from customer_order_app.models import OrderModel
from .serializers import OrderSerializer, CreateOrderSerializer, UpdateSerializer
from .permissions import IsOrderOwner, IsCustomer

""" View that handles incommig POST or GET requests for orders. """
class OrderViewSet(generics.ListCreateAPIView):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    """ Method to set different permissions based on request method. """
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsCustomer()]
        return [IsAuthenticated()]

    """ Function that decides serializer-class depending of request type. """
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        return OrderSerializer

    """ Function to list all orders """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    """ Function to create new order entry. """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        output_serializer = OrderSerializer(order)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

""" View to handle GET, PATCH and DELETE requests. """
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwner]

    """ Function that decides serializer-class depending of request type. """
    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateSerializer
        return OrderSerializer

    """ Function to patch existing order. """
    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        output_serializer = OrderSerializer(order)
        return Response(output_serializer.data)

""" View for GET requests to list all orders excepting completed orders. """
class OrderCountView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        business_user_id = self.kwargs.get('business_user_id')
        get_object_or_404(User, id=business_user_id)

        order_count = OrderModel.objects.filter(
            business_user_id=business_user_id,
            status__in=['pending', 'in_progress']
        ).count()

        return Response({'order_count': order_count})

""" View for GET requests to list all status compoleted orders. """
class OrderCountCompletedView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        business_user_id = self.kwargs.get('business_user_id')
        get_object_or_404(User, id=business_user_id)

        order_count = OrderModel.objects.filter(
            business_user_id=business_user_id,
            status__in=['completed']
        ).count()

        return Response({"completed_order_count": order_count})