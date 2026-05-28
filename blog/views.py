from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.db.models import Q


# 1. 🌸 Home Feed Grid Stream View (The one Django was missing!)
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
# 📝 Updated UpdateView inside blog/views.py
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
