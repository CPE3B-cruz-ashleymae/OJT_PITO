from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # This adds columns for Title, Author, and Date
    list_display = ('title', 'author', 'date_posted')
    
    # This adds a filter sidebar on the right
    list_filter = ('date_posted', 'author')
    
    # This adds a search bar at the top
    search_fields = ('title', 'content')