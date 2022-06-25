from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from user.views import SignUpApiView, UserManagementApiView, UserResetPasswordApiView
from rest_framework.routers import DefaultRouter, SimpleRouter

# router = SimpleRouter()
# 
# router.register('reset-password', UserResetPasswordApiView, basename='reset-password')


app_name = 'user'

urlpatterns = [
    # path('', include(router.urls)),
    path('signup/', SignUpApiView.as_view(), name='signup'),
    path('signin/', TokenObtainPairView.as_view(), name='signin'),
    path('reset-password/', UserResetPasswordApiView.as_view(), name='reset-password'),
    path('profile/', UserManagementApiView.as_view(), name='profile')
]