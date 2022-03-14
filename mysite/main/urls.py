"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = "main"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("login/", views.login_request, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("driver/", views.driver, name="driver"),
    path("patient-delivered/", views.patient_delivered, name="patient_delivered"),
    path("resend_otp/", views.resend_otp, name="resend_otp"),
    path("driver-verification/", views.driver_verification,
         name="driver_verification"),
         
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='main/password_reset.html', success_url=reverse_lazy('main/password_reset_done.html')), name='password_reset'),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="main/password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="main/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name="main/password_reset_complete.html"), name="password_reset_complete"),


]
