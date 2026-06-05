from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from reviews_app.models import ReviewModel
from user_auth_app.models import UserProfile
from .serializers import ReviewSerializer, UpdateSerializer
from .permissions import IsCustomer, IsReviewAuthorOrReadOnly

class ReviewListView(generics.ListCreateAPIView):
    """ Handles GET and POST requests for reviews. """

    queryset = ReviewModel.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = None

    def get_permissions(self):
        """ Handels permissions depending of request-type. """
        if self.request.method == "POST":
            return [IsAuthenticated(), IsCustomer()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """ Creates review via POST request. """
        reviewer_profile = UserProfile.objects.get(user=self.request.user)
        serializer.save(user=self.request.user, reviewer=reviewer_profile)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ handles PATCH and DELETE requests for specific reviews. """

    queryset = ReviewModel.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewAuthorOrReadOnly]

    def get_serializer_class(self):
        """ Handles serializers depending of request type. """
        if self.request.method == "PATCH":
            return UpdateSerializer
        return ReviewSerializer

    def partial_update(self, request, *args, **kwargs):
        """ Handles PATCH request for partial review fields. """
        kwargs['partial'] = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()

        output_serializer = ReviewSerializer(review)
        return Response(output_serializer.data)