from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    Signup endpoint using Django's built-in User model.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {"detail": "username and password are required"},
            status=400,
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"detail": "User with this username already exists"},
            status=400,
        )

    user = User.objects.create_user(username=username, password=password)

    # Optionally return tokens right after signup
    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "success": True,
            "message": "User created successfully",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        },
        status=201,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Login endpoint that returns SimpleJWT access/refresh tokens.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {"detail": "username and password are required"},
            status=400,
        )

    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({"detail": "Invalid credentials"}, status=401)

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        },
        status=200,
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Hello(request):
    """
    Simple authenticated test endpoint.
    """
    return Response(f"Hello, {request.user.username}")