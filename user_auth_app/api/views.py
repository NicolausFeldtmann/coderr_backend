from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from user_auth_app.models import UserProfile
from .serializers import RegistrationSerializer, UsernameAuthSerializer, UserProfileSerializer, SingleUserSerializer, BusinessProfileSerializer, CustomerProfileSerializer
from .permissions import IsOwnerOrAdmin

""" View to handle GET, PATCH and DELETE requests. """
class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

""" View to handle GET requestes for business-profiles only. """
class BusinessProfileListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BusinessProfileSerializer
    pagination_class = None

    def get_queryset(self):
        return UserProfile.objects.filter(role='business')

""" View to handle GET requestes for customer-profiles only. """
class CustomerProfileListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerProfileSerializer
    pagination_class = None

    def get_queryset(self):
        return UserProfile.objects.filter(role='customer')

""" View to handle POST request for registration attempt. """
class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

""" View to handle login attempt with username/password combination or authtoken. """
class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]
    serializer_class = UsernameAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        data = {}
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, create = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id
            }
        else:
            return Response({"error": "Wrong username or password."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data)