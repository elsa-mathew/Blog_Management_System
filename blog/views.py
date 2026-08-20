from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Category, Tag, Comment, Like
from django.contrib.auth.models import User
from django.contrib import messages

def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        tags = request.POST.getlist('tags')
        status = request.POST.get('status')

        category = Category.objects.get(id=category_id)
        post = Post.objects.create(
            user=request.user,
            author=request.user.username,
            title=title,
            content=content,
            category=category,
            status=status
        )
        post.tags.set(tags)
        messages.success(request, 'Post created successfully!')
        return redirect('home')

    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'create_post.html', {'categories': categories, 'tags': tags})

def view_post(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = post.comments.all()
    likes_count = post.likes.count()
    user_liked = post.likes.filter(user=request.user).exists() if request.user.is_authenticated else False

    if request.method == 'POST':
        if 'comment' in request.POST:
            content = request.POST.get('content')
            Comment.objects.create(post=post, user=request.user, content=content)
            messages.success(request, 'Comment added successfully!')
            return redirect('view_post', post_id=post.id)

        elif 'like' in request.POST:
            if user_liked:
                Like.objects.filter(post=post, user=request.user).delete()
                messages.success(request, 'You unliked the post.')
            else:
                Like.objects.create(post=post, user=request.user)
                messages.success(request, 'You liked the post.')
            return redirect('view_post', post_id=post.id)

    return render(request, 'view_post.html', {'post': post, 'comments': comments, 'likes_count': likes_count, 'user_liked': user_liked})

def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        category_id = request.POST.get('category')
        tags = request.POST.getlist('tags')
        post.status = request.POST.get('status')

        post.category = Category.objects.get(id=category_id)
        post.tags.set(tags)
        post.save()
        messages.success(request, 'Post updated successfully!')
        return redirect('view_post', post_id=post.id)

    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'edit_post.html', {'post': post, 'categories': categories, 'tags': tags})

def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('home')
    return render(request, 'delete_post.html', {'post': post})

