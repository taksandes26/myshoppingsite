from django.urls import path
from .views import SignUpView, LoginView, DashboardView, LogoutView

app_name = "accounts"
urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),


]
