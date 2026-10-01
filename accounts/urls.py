from django.urls import path
from .views import SignUpView
from django.contrib.auth import views as auth_views

#urls para el sistema de cuentas (login, logout, registro)
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("signup/", SignUpView.as_view(), name='signup'),
]
