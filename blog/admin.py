from django.contrib import admin
from .models import Category, Tag, Post, Comment, Like


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'category',
        'status',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'status',
        'category',
        'created_at',
    )

    search_fields = (
        'title',
        'content',
        'author__username',
    )

    prepopulated_fields = {
        'slug': ('title',)
    }


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'user',
        'created_at',
    )

    list_filter = ('created_at',)

    search_fields = (
        'content',
        'user__username',
        'post__title',
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'user',
        'created_at',
    )

    search_fields = (
        'post__title',
        'user__username',
    )