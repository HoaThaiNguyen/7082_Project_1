from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Event


@api_view(['POST'])
@permission_classes([AllowAny])
def api_signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    if not username or not password:
        return Response({'detail': 'Username and password required'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'detail': 'User already exists'}, status=400)

    user = User.objects.create_user(
        username=username, email=email, password=password)
    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'username': user.username,
    }, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_events(request):
    qs = Event.objects.filter(user=request.user).values('id', 'name', 'date')
    return Response({'events': list(qs)})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    return Response({
        'username': request.user.username,
        'email': request.user.email
    })
