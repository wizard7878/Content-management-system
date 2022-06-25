from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import UpdateModelMixin, ListModelMixin
from core.models import User
from user.serializer import UserSerializer, ResetPasswordSerializer, UserProfileManagerSerializer
# Create your views here.


class SignUpApiView(generics.CreateAPIView):
    """
    User sign up api view
    """
    serializer_class = UserSerializer


class UserManagementApiView(generics.RetrieveUpdateAPIView):
    """
    Retrieve User data and update them
    """
    serializer_class = UserProfileManagerSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user


class UserResetPasswordApiView(generics.UpdateAPIView):
    """
    Update or reset password
    """
    
    permission_classes = (IsAuthenticated, )
    serializer_class = ResetPasswordSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    

    
