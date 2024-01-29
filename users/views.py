from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.contrib.gis.geos import Point
from .models import Customer
from .serializers import CustomerSerializer, UserSerializer

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data.get('user'))
        customer_serializer = self.get_serializer(data=request.data)

        user_serializer.is_valid(raise_exception=True)
        customer_serializer.is_valid(raise_exception=True)

        # Create User instance
        user = User.objects.create_user(**user_serializer.validated_data)

        # Extract latitude and longitude from the request data
        latitude = request.data.get('latitude', None)
        longitude = request.data.get('longitude', None)

        # Check if both latitude and longitude are present
        if latitude is not None and longitude is not None:
            # Create a Point object with the given latitude and longitude
            location = Point(float(longitude), float(latitude))
            customer_serializer.validated_data['location'] = location

        # Create Customer instance
        customer_serializer.validated_data['user'] = user
        self.perform_create(customer_serializer)

        # Create and return token
        token, created = Token.objects.get_or_create(user=user)


        headers = self.get_success_headers(customer_serializer.data)
        return Response({'token': token.key, **customer_serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class UserLoginView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            return Response({'token': token.key, **serializer.data})
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)