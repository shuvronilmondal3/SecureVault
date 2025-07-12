from django.urls import path
from .views import WelcomeView,SignupView, NotesView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import VaultPasswordView
from .views import VaultFileUploadView
from .views import verify_otp
from .views import LoginView
urlpatterns = [
    path('welcome/', WelcomeView.as_view(), name='welcome'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('notes/', NotesView.as_view(), name='notes'),
    path('vault-passwords/', VaultPasswordView.as_view(), name='vault-passwords'),
    path('vault-files/', VaultFileUploadView.as_view(), name='vault-files'),
    path('verify-otp/', verify_otp, name='verify-otp'),
    # path('login/', LoginView.as_view(), name='login'),


]
