from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status   
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Note
from .serializers import NoteSerializer
from .models import VaultPassword
from .serializers import VaultPasswordSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .models import VaultFile
from .serializers import VaultFileSerializer
from .utils.otp import generate_otp
from .models import UserOTP
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView

class WelcomeView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to SecureVault!"})


User = get_user_model()

class SignupView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=400)

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )
        return Response({'message': 'User created successfully'}, status=201)

class NotesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notes = Note.objects.filter(user=request.user).order_by('-created_at')
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VaultPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        passwords = VaultPassword.objects.filter(user=request.user)
        serializer = VaultPasswordSerializer(passwords, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VaultPasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class VaultFileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file uploaded"}, status=400)
        vault_file = VaultFile.objects.create(user=request.user, file=file_obj)
        serializer = VaultFileSerializer(vault_file)
        return Response(serializer.data, status=201)

    def get(self, request):
        files = VaultFile.objects.filter(user=request.user)
        serializer = VaultFileSerializer(files, many=True)
        return Response(serializer.data)
    
class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(username=request.data['username'])

            if user.is_2fa_enabled:
                otp_code = generate_otp(user)
                print(f"🔐 OTP for {user.username}: {otp_code}")  # simulate email
                return Response({"detail": "OTP sent", "2fa": True}, status=202)

            return super().post(request, *args, **kwargs)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
@api_view(['POST'])
@permission_classes([])
def verify_otp(request):
    username = request.data.get("username")
    code = request.data.get("code")

    try:
        user = User.objects.get(username=username)
        otp = UserOTP.objects.get(user=user)

        if otp.code == code and otp.is_valid():
            # OTP success: return JWT token
            refresh = RefreshToken.for_user(user)
            otp.delete()  # prevent reuse
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        else:
            return Response({"error": "Invalid or expired OTP"}, status=400)

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    except UserOTP.DoesNotExist:
        return Response({"error": "OTP not generated"}, status=400)
