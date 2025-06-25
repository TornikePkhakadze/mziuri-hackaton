from rest_framework.viewsets import ViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import User
from rest_framework.permissions import IsAuthenticated
from .serializer import UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .serializer import RegisterSerializer  
from .serializer import DepositForm

User = get_user_model()

class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

class CreateUser(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class RegisterViewSet(CreateModelMixin,GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LoginViewSet(ViewSet):
    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email,
        }, status=status.HTTP_200_OK)
    
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')  
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)  
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterSerializer(data=request.POST) 
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return redirect('loginn')
        else:
            messages.error(request, "Registration failed.")
    else:
        form = RegisterSerializer()  

    return render(request, 'register.html', {'form': form})

def profile_view(request):
    return render(request, 'profile.html')

def account_view(request):
    return render(request, 'account.html')

def home_view(request):
    return render(request, "home.html")

@login_required
def purchase_history(request):
    purchases = request.user.purchases.all().order_by('-created_at')  
    return render(request, 'purchase_history.html', {'purchases': purchases})

@login_required
def deposit_money(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            request.user.money += amount
            request.user.save()
            messages.success(request, f"${amount} deposited successfully.")
            return redirect('shop') 
    else:
        form = DepositForm()
    
    return render(request, 'deposit.html', {'form': form})
