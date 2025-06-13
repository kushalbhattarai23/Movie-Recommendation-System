from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .models import *
from .serializers import *
from .models import Cinema, MovieRating
from .serializers import MovieSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer

class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # Number of movies per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Cinema.objects.all()
    serializer_class = MovieSerializer
    pagination_class = StandardResultsSetPagination
    
    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'rating' not in request.data:
            return Response({'error': 'Rating is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        movie = self.get_object()
        user = request.user
        rating = request.data['rating']
        
        rating_instance, created = Rating.objects.get_or_create(
            user=user,
            movie=movie,
            defaults={'rating': rating}
        )
        
        if not created:
            rating_instance.rating = rating
            rating_instance.save()
            
        return Response({'message': 'Rating saved'})

    

class RequestPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            token = get_random_string(32)
            PasswordResetToken.objects.create(user=user, token=token)
            
            reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
            send_mail(
                'Password Reset Request',
                f'Click the following link to reset your password: {reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Password reset email sent'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class PasswordResetConfirmView(APIView):
    def post(self, request):
        token = request.data.get('token')
        password = request.data.get('password')
        
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
            user = reset_token.user
            user.set_password(password)
            user.save()
            reset_token.delete()
            return Response({'message': 'Password reset successful'})
        except PasswordResetToken.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            
class MovieRatingViewSet(viewsets.ModelViewSet):
    queryset = MovieRating.objects.all()
    serializer_class = MovieRatingSerializer



from .recommendations import MovieRecommender

class MovieDetailView(RetrieveAPIView):
    queryset = Cinema.objects.all()
    serializer_class = MovieSerializer
    

    
class MovieListView(APIView):
    def get(self, request, *args, **kwargs):
        movies = Cinema.objects.all()  # Adjust the queryset as needed
        serializer = MovieSerializer(movies, many=True)
        return Response({"results": serializer.data})