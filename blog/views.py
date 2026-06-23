from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, UserProfile, Education, WorkExperience, Skill
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import PDSForm
import json

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(content__icontains=query))
        return queryset

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = 'blog/post_form.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = 'blog/post_form.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        return self.request.user.is_superuser or (self.request.user == post.author)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog-home')
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('blog-home')
    return render(request, 'users/login.html', {'form': AuthenticationForm()})

def about(request):
    return render(request, 'blog/about.html')

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('blog-home')

    search_query = request.GET.get('q', '').strip()
    pds_results = None

    if search_query:
        pds_results = UserProfile.objects.filter(
            Q(first_name__icontains=search_query) |
            Q(surname__icontains=search_query) |
            Q(res_city_name__icontains=search_query) |
            Q(res_province_name__icontains=search_query) |
            Q(res_barangay_name__icontains=search_query) |
            Q(per_city_name__icontains=search_query) |
            Q(per_province_name__icontains=search_query) |
            Q(mobile_number__icontains=search_query) |
            Q(email_address__icontains=search_query) |
            Q(citizenship__icontains=search_query) |
            Q(user__username__icontains=search_query)
        ).select_related('user')

    users = User.objects.all().order_by('username')
    posts = Post.objects.all().order_by('-date_posted')

    context = {
        'users': users,
        'posts': posts,
        'total_users': users.count(),
        'total_posts': posts.count(),
        'search_query': search_query,
        'pds_results': pds_results,
    }
    return render(request, 'blog/admin_dashboard.html', context)

@login_required
def pds_page(request):
    profile = request.user.userprofile
    educations = profile.educations.all()
    work_experiences = profile.work_experiences.all()
    skills = profile.skills.all()
    edu_dict = {e.level: e for e in educations}
    context = {
        'profile': profile,
        'edu_dict': edu_dict,
        'work_experiences': work_experiences,
        'skills': skills,
        'education_levels': ['Elementary', 'Secondary', 'College', 'Vocational'],
    }
    return render(request, 'blog/pds_page.html', context)

@login_required
def pds_update(request):
    if request.method == 'POST':
        profile = request.user.userprofile
        p = request.POST
        profile.surname = p.get('surname', '')
        profile.first_name = p.get('first_name', '')
        profile.middle_name = p.get('middle_name', '')
        profile.name_extension = p.get('name_extension', '')
        profile.age = p.get('age', '')
        profile.dob = p.get('dob') or None
        profile.place_of_birth = p.get('place_of_birth', '')
        profile.sex = p.get('sex', 'Male')
        profile.civil_status = p.get('civil_status', 'Single')
        profile.height = p.get('height', '')
        profile.weight = p.get('weight', '')
        profile.blood_type = p.get('blood_type', 'N/A')
        profile.citizenship = p.get('citizenship', 'Filipino')

        # Residential Address — save both code and display name
        profile.res_house_no      = p.get('res_house_no', '')
        profile.res_street        = p.get('res_street', '')
        profile.res_subdivision   = p.get('res_subdivision', '')
        profile.res_barangay      = p.get('res_barangay', '')
        profile.res_barangay_name = p.get('res_barangay_name', '')
        profile.res_city          = p.get('res_city', '')
        profile.res_city_name     = p.get('res_city_name', '')
        profile.res_province      = p.get('res_province', '')
        profile.res_province_name = p.get('res_province_name', '')
        profile.res_zip           = p.get('res_zip', '')

        profile.same_as_residential = 'same_as_residential' in p

        if profile.same_as_residential:
            profile.per_house_no      = profile.res_house_no
            profile.per_street        = profile.res_street
            profile.per_subdivision   = profile.res_subdivision
            profile.per_barangay      = profile.res_barangay
            profile.per_barangay_name = profile.res_barangay_name
            profile.per_city          = profile.res_city
            profile.per_city_name     = profile.res_city_name
            profile.per_province      = profile.res_province
            profile.per_province_name = profile.res_province_name
            profile.per_zip           = profile.res_zip
        else:
            profile.per_house_no      = p.get('per_house_no', '')
            profile.per_street        = p.get('per_street', '')
            profile.per_subdivision   = p.get('per_subdivision', '')
            profile.per_barangay      = p.get('per_barangay', '')
            profile.per_barangay_name = p.get('per_barangay_name', '')
            profile.per_city          = p.get('per_city', '')
            profile.per_city_name     = p.get('per_city_name', '')
            profile.per_province      = p.get('per_province', '')
            profile.per_province_name = p.get('per_province_name', '')
            profile.per_zip           = p.get('per_zip', '')

        profile.telephone     = p.get('telephone', 'N/A')
        profile.mobile_number = p.get('mobile_number', '')
        profile.email_address = p.get('email_address', '')
        profile.save()
        messages.success(request, "Personal information saved successfully!")
    return redirect('pds-page')

@login_required
def pds_save_education(request):
    if request.method == 'POST':
        profile = request.user.userprofile
        p = request.POST
        for level in ['Elementary', 'Secondary', 'College', 'Vocational']:
            school = p.get(f'edu_school_{level}', '').strip()
            degree = p.get(f'edu_degree_{level}', '').strip()
            year   = p.get(f'edu_year_{level}', '').strip()
            Education.objects.update_or_create(
                user_profile=profile,
                level=level,
                defaults={'school_name': school, 'degree': degree, 'year_graduated': year}
            )
        messages.success(request, "Education saved successfully!")
    return redirect('pds-page')

@login_required
def pds_save_work(request):
    if request.method == 'POST':
        profile = request.user.userprofile
        p = request.POST
        company          = p.get('company', '').strip()
        position         = p.get('position', '').strip()
        date_from        = p.get('date_from') or None
        date_to          = p.get('date_to') or None
        currently_working = 'currently_working' in p
        if company or position:
            WorkExperience.objects.create(
                user_profile=profile,
                company=company,
                position=position,
                date_from=date_from,
                date_to=date_to,
                currently_working=currently_working,
            )
            messages.success(request, "Work experience added!")
    return redirect('pds-page')

@login_required
def pds_delete_work(request, work_id):
    work = get_object_or_404(WorkExperience, id=work_id, user_profile=request.user.userprofile)
    work.delete()
    return redirect('pds-page')

@login_required
def pds_save_skill(request):
    if request.method == 'POST':
        profile    = request.user.userprofile
        skill_name = request.POST.get('skill_name', '').strip()
        if skill_name:
            Skill.objects.create(user_profile=profile, name=skill_name)
            messages.success(request, "Skill added!")
    return redirect('pds-page')

@login_required
def pds_save_emergency(request):
    if request.method == 'POST':
        profile = request.user.userprofile
        p = request.POST
        profile.emergency_name         = p.get('emergency_name', '')
        profile.emergency_relationship = p.get('emergency_relationship', '')
        profile.emergency_phone        = p.get('emergency_phone', '')
        profile.emergency_address      = p.get('emergency_address', '')
        profile.save()
        messages.success(request, "Emergency contact saved!")
    return redirect('pds-page')

@user_passes_test(lambda u: u.is_superuser)
def toggle_user_status(request, user_id):
    u = get_object_or_404(User, id=user_id)
    if not u.is_superuser:
        u.is_active = not u.is_active
        u.save()
    return redirect('admin_dashboard')

@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    u = get_object_or_404(User, id=user_id)
    if not u.is_superuser:
        u.delete()
    return redirect('admin_dashboard')

def user_profile_view(request, username):
    viewed_user = get_object_or_404(User, username=username)
    profile     = viewed_user.userprofile
    educations  = profile.educations.all()
    work_experiences = profile.work_experiences.all()
    skills      = profile.skills.all()
    edu_dict    = {e.level: e for e in educations}
    context = {
        'viewed_user': viewed_user,
        'profile': profile,
        'edu_dict': edu_dict,
        'education_levels': ['Elementary', 'Secondary', 'College', 'Vocational'],
        'work_experiences': work_experiences,
        'skills': skills,
    }
    return render(request, 'blog/user_profile.html', context)