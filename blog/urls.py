from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('admin-dashboard/toggle-user/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('admin-dashboard/delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('pds/', views.pds_page, name='pds-page'),
    path('pds/update/', views.pds_update, name='pds-update'),
    path('pds/save-education/', views.pds_save_education, name='pds-save-education'),
    path('pds/save-work/', views.pds_save_work, name='pds-save-work'),
    path('pds/delete-work/<int:work_id>/', views.pds_delete_work, name='pds-delete-work'),
    path('pds/save-skill/', views.pds_save_skill, name='pds-save-skill'),
    path('pds/save-emergency/', views.pds_save_emergency, name='pds-save-emergency'),
    path('user/<str:username>/', views.user_profile_view, name='user-profile'),  
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
