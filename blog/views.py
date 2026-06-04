from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.db.models import Q

# Added imports for the Custom Admin Dashboard
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages




# 1. 🌸 Home Feed Grid Stream View
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # Adjust to match your app structure
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2  # Keeps your pagination intact!

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')  # 🔍 Grabs the text from the search bar
        if query:
            # Filters posts where the title OR content contains the search phrase
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        return queryset


# 2. 🔍 Single Post In-Depth Detail View
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


# 3. ✍️ Create View for Publishing Brand New Posts
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# 4. 📝 Secure Update View for Authors to Edit Posts
class PostUpdateView(LoginRequiredMixin, UpdateView): # 💡 Removed UserPassesTestMixin
    model = Post
    fields = ['title', 'content', 'image'] # 💡 Added 'image' field here if your Post model has one
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        
    # 💡 Removed test_func() completely so anyone can edit any post


# 5. 🗑️ Secure Deletion View for Removing Posts
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog-home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


# =========================================================================
# 🛠️ CUSTOM ADMINISTRATIVE DASHBOARD VIEWS (Supervisor Task Requirements)
# =========================================================================

# Helper Guard: Only allow logged-in administrators/superusers to access these views
def admin_required(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(admin_required, login_url='login')
def admin_dashboard(request):
    """
    Displays the secure user matrix dashboard.
    Password hashes and sensitive data are strictly excluded from the query selection.
    """
    users = User.objects.all().only(
        'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active'
    ).order_by('-date_joined')
    
    context = {
        'users': users,
    }
    return render(request, 'blog/admin_dashboard.html', context)


@user_passes_test(admin_required, login_url='login')
def toggle_user_status(request, user_id):
    """Allows admin to activate/deactivate accounts smoothly."""
    user_to_manage = get_object_or_404(User, id=user_id)
    if user_to_manage.is_superuser:
        messages.error(request, "You cannot deactivate another administrator.")
    else:
        user_to_manage.is_active = not user_to_manage.is_active
        user_to_manage.save()
        status = "activated" if user_to_manage.is_active else "deactivated"
        messages.success(request, f"User {user_to_manage.username} has been successfully {status}.")
    return redirect('admin_dashboard')


@user_passes_test(admin_required, login_url='login')
def delete_user(request, user_id):
    """Allows admin to safely delete accounts from the dashboard matrix."""
    user_to_manage = get_object_or_404(User, id=user_id)
    if user_to_manage.is_superuser:
        messages.error(request, "You cannot delete an administrator account.")
    else:
        username = user_to_manage.username
        user_to_manage.delete()
        messages.success(request, f"Account {username} has been permanently deleted.")
    return redirect('admin_dashboard')