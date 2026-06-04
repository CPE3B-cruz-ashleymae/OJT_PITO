from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from users import views as user_views

# Helper function to check if the user is a superuser/admin
def admin_required(user):
    return user.is_authenticated and user.is_superuser

# Custom view to explicitly catch /admin/ attempts and block them
def disabled_admin_view(request):
    return redirect('admin_dashboard')

urlpatterns = [
    path('admin/', disabled_admin_view),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    
    # --- UPDATED: Using your custom login_view for redirect logic ---
    path('login/', user_views.login_view, name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # django-allauth Social Authentication
    path('accounts/', include('allauth.urls')),

    # Password Reset Flow
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    # Main Application
    path('', include('blog.urls')),
]