from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


# =====================================
# REGISTER SERIALIZER
# =====================================

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    password2 = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
            "password",
            "password2"
        ]

    # ==============================
    # VALIDATE USERNAME
    # ==============================

    def validate_username(self, value):

        if User.objects.filter(username=value).exists():

            raise serializers.ValidationError(
                "Username already taken."
            )

        return value

    # ==============================
    # VALIDATE EMAIL
    # ==============================

    def validate_email(self, value):

        if User.objects.filter(email=value).exists():

            raise serializers.ValidationError(
                "Email already registered."
            )

        return value

    # ==============================
    # VALIDATE PASSWORDS
    # ==============================

    def validate(self, data):

        if data["password"] != data["password2"]:

            raise serializers.ValidationError(
                {
                    "password": "Passwords do not match."
                }
            )

        return data

    # ==============================
    # CREATE USER
    # ==============================

    def create(self, validated_data):

        validated_data.pop("password2")

        password = validated_data.pop("password")

        user = User.objects.create(
            **validated_data
        )

        user.set_password(password)

        user.save()

        return user


# =====================================
# PROFILE SERIALIZER
# =====================================

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "profile_image",
            "created_at"
        ]

        read_only_fields = [
            "username",
            "email",
            "created_at"
        ]


# =====================================
# JWT LOGIN SERIALIZER
# =====================================

class CustomTokenObtainPairSerializer(
    TokenObtainPairSerializer
):

    username_field = "email"

    @classmethod
    def get_token(cls, user):

        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email

        return token

    def validate(self, attrs):

        attrs["username"] = attrs.get("email")

        data = super().validate(attrs)

        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
        }

        return data