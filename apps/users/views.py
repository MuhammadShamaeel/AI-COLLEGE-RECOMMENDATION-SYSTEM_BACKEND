from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

from .serializers import (
    RegisterSerializer,
    UserProfileSerializer,
    CustomTokenObtainPairSerializer
)


# =====================================
# REGISTER VIEW
# =====================================

class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "User registered successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


# =====================================
# LOGIN VIEW
# =====================================

class CustomLoginView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer


# =====================================
# USER PROFILE VIEW
# =====================================

class UserProfileView(APIView):

    permission_classes = [IsAuthenticated]

    # GET PROFILE
    def get(self, request):

        serializer = UserProfileSerializer(
            request.user
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )

    # UPDATE PROFILE
    def put(self, request):

        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Profile updated successfully",
                    "data": serializer.data
                }
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )