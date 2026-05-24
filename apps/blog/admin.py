from django.contrib import admin

from .models import BlogPost, Category, Comment, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'is_featured', 'published_at')
    list_filter = ('status', 'category', 'is_featured')
    list_editable = ('status', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    filter_horizontal = ('tags',)
    date_hierarchy = 'published_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'post', 'is_approved', 'created_at')
    list_filter = ('is_approved',)
    list_editable = ('is_approved',)
    search_fields = ('author_name', 'content')
