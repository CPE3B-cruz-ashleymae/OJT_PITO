from django.contrib import admin
from .models import Post, UserProfile, WorkExperience, Education, CivilServiceEligibility, TrainingProgram

# Define the Inline models for one-to-many relationships
class WorkExperienceInline(admin.StackedInline):
    model = WorkExperience
    extra = 1

class EducationInline(admin.StackedInline):
    model = Education
    extra = 1

class CivilServiceEligibilityInline(admin.StackedInline):
    model = CivilServiceEligibility
    extra = 1

class TrainingProgramInline(admin.StackedInline):
    model = TrainingProgram
    extra = 1

# Register the main Profile model with all its associated PDS inlines
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    inlines = [
        WorkExperienceInline, 
        EducationInline, 
        CivilServiceEligibilityInline, 
        TrainingProgramInline
    ]
    list_display = ('user', 'surname', 'mobile_number')
    search_fields = ('user__username', 'surname')

# Register the Post model
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted')
    list_filter = ('date_posted', 'author')
    search_fields = ('title', 'content')