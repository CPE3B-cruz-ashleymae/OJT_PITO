from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

# Helper function to check if the user is a superuser/admin
def admin_required(user):
    return user.is_authenticated and user.is_superuser

# Custom view to explicitly catch /admin/ attempts and block them
def disabled_admin_view(request):
    # This prevents anyone from accessing the default panel, even if they guess the URL
    return redirect('admin_dashboard')

urlpatterns = [
    # 1. Disable the default Django Admin completely
    path('admin/', disabled_admin_view),
    
    # 2. Include your app's URLs (Assuming your app name is 'blog' or similar)
    path('', include('blog.urls')),
]