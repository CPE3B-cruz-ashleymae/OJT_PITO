from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from users import views as user_views
from blog import views as blog_views

# Redirect /admin/ to custom login instead of Django admin
admin.site.login = lambda request, **kwargs: redirect('login')

urlpatterns = [
    # --- DASHBOARD & LOGIN/LOGOUT ---
    path('admin-dashboard/', blog_views.admin_dashboard, name='admin_dashboard'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.custom_logout, name='logout'),

    # --- ADMIN ROUTES (disabled for non-superusers) ---
    path('admin/', admin.site.urls),

    # --- USER ACTIONS ---
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),

    # --- SOCIAL & AUTHENTICATION ---
    path('accounts/', include('allauth.urls')),

    # --- PASSWORD RESET FLOW ---
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

    # --- MAIN APPLICATION ---
    path('', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
