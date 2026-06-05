from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework import serializers
from user_auth_app.models import UserProfile

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    """ Converts all needed field-datas for UserProfiles. """

    type = serializers.CharField(source='role')

    class Meta:
        model = UserProfile
        fields = [
            "user", 
            "username", 
            "first_name", 
            "last_name",
            "file", 
            "location", 
            "tel", 
            "description",
            "working_hours", 
            "type", 
            "email", 
            "created_at"
        ]

class SingleUserSerializer(serializers.ModelSerializer):
    """ Converts all needed field-data for single UserProfile. """

    type = serializers.CharField(source='role')

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type"
        ]

class RegistrationSerializer(serializers.Serializer):
    """ Converts all needed incomming data to create UserProfieles.  """
    """ New user decides own user type. """
    """ Validates given email adress and passwords. """

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True,default="")
    last_name = serializers.CharField(required=False, allow_blank=True, default="")
    type = serializers.ChoiceField(choices=[("customer", "Customer"), ("business", "Business")], default="customer")

    def validate_email(self, value):
        """ Function validates if email is valid email or is already in use. """

        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError({"error": "Invalid email."})

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError({"error": "Email already exists."})
        return value

    def validate(self, data):
        """ Validates incomming data. Converts username if necesery. """

        if data.get("password") != data.get("repeated_password"):
            raise serializers.ValidationError({"error": "Passwords don't match."})
        
        original_username = self.initial_data.get("username", "")

        if " " in original_username:
            parts = original_username.strip().split(" ", 1)
            if len(parts) == 2:
                data["first_name"] = parts[0]
                data["last_name"] = parts[1]
            elif len(parts) == 1:
                data["first_name"] = parts[0]
                data["last_name"] = ""
        return data

    def create(self, validated_data):
        """ Function creates user-account if all data are valid. """

        password = validated_data.pop("password")
        validated_data.pop("repeated_password", None)
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        first_name = validated_data.pop("first_name", "")
        last_name = validated_data.pop("last_name", "")
        role = validated_data.pop("type", "customer")

        user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        UserProfile.objects.create(user=user, username=username, first_name=first_name, last_name=last_name, email=email, role=role)
        return user


class UsernameAuthSerializer(serializers.Serializer):
    """ Converts incommig data for login. """
    """ Validates combination of correct username and password. """

    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"}, trim_whitespace=False)

    def validate(self, attrs):
        """ Validates username and password combination. """
        username = attrs.get("username")
        password = attrs.get("password")

        try:
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "invalid access"})
        if not user.check_password(password):
            raise serializers.ValidationError({"error": "invalid access"})

        attrs["user"] = user
        return attrs   

class BusinessProfileSerializer(serializers.ModelSerializer):
    """ Serializer for business-profiles. """

    type = serializers.CharField(source='role', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type"
        ]


class CustomerProfileSerializer(serializers.ModelSerializer):
    """ Serializer for customer-profiles. """

    type = serializers.CharField(source='role', read_only=True)
    uploaded_at = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "uploaded_at",
            "type"
        ]