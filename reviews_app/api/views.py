from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from reviews_app.models import ReviewModel
from .serializers import ReviewSerializer, UpdateSerializer
from .permissions import IsCustomer, IsReviewAuthorOrReadOnly

""" Handles GET and POST requests for reviews. """
class ReviewListView(generics.ListCreateAPIView):
    queryset = ReviewModel.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = None

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsCustomer()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()

""" handles PATCH and DELETE requests for specific reviews. """
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReviewModel.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateSerializer
        return ReviewSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()

        output_serializer = ReviewSerializer(review)
        return Response(output_serializer.data)