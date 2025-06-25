from django.urls import path
from .views import register_view
from django.urls import path 
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CreateUser, RegisterViewSet, LoginViewSet
from .views import account_view , login_view, home_view , profile_view , deposit_money



router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("createuser", CreateUser, basename="createuser")
router.register('register', RegisterViewSet, basename='register')
router.register('login', LoginViewSet, basename='login')
urlpatterns=[
    path('', account_view, name='account'),
    path("loginn/", login_view, name='loginn'),
    path('registerr/', register_view, name='registerr'),
    path('home/', home_view, name='home'),
    path('user/', profile_view, name='user'),
    path('deposit/', deposit_money, name='deposit_money'),
]




