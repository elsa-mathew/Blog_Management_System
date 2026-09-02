from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Category, Tag, Comment, Like
from .models import Post, Category, Like, Comment
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import PostForm
from django.db.models import Q
from .forms import PostForm, EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
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

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Post, Like, Comment

@login_required
def dashboard(request):

    user_posts = Post.objects.filter(
        author=request.user
    )

    search_query = request.GET.get('q', '').strip()

    recent_posts = user_posts.order_by(
        '-created_at'
    )

    if search_query:
        recent_posts = recent_posts.filter(
            Q(title__icontains=search_query)
            | Q(content__icontains=search_query)
        )

    context = {
        'total_posts': user_posts.count(),

        'draft_posts': user_posts.filter(
            status='draft'
        ).count(),

        'total_likes': Like.objects.filter(
            post__author=request.user
        ).count(),

        'total_comments': Comment.objects.filter(
            post__author=request.user
        ).count(),

        'recent_posts': recent_posts[:5],

        'search_query': search_query,
    }

    return render(
        request,
        'user/dashboard.html',
        context
    )
@login_required
def blog_feed(request):

    category_slug = request.GET.get(
        'category',
        ''
    ).strip()

    posts = Post.objects.filter(
        status='published'
    ).select_related(
        'author',
        'category'
    ).prefetch_related(
        'likes',
        'comments',
        'tags'
    )

    if category_slug:
        posts = posts.filter(
            category__slug=category_slug
        )

    categories = Category.objects.all().order_by('name')

    liked_post_ids = set(
        Like.objects.filter(
            user=request.user,
            post__in=posts
        ).values_list(
            'post_id',
            flat=True
        )
    )

    return render(
        request,
        'user/home.html',
        {
            'posts': posts,
            'liked_post_ids': liked_post_ids,
            'categories': categories,
            'selected_category': category_slug,
        }
    )


@login_required
def create_post(request):

    if request.method == 'POST':

        form = PostForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            post = form.save(commit=False)

            
            post.author = request.user
            
           
            if 'publish' in request.POST:
                post.status = 'published'
            else:
                post.status = 'draft'

            
            from django.utils.text import slugify

            base_slug = slugify(post.title)
            slug = base_slug
            counter = 2

            while Post.objects.filter(slug=slug).exists():

                slug = f'{base_slug}-{counter}'
                counter += 1

            post.slug = slug

            post.save()

        
            form.save_m2m()

            if post.status == 'published':

                messages.success(
                    request,
                    'Your post has been published successfully!'
                )

            else:

                messages.success(
                    request,
                    'Your post has been saved as a draft.'
                )

            return redirect('blog_feed')

    else:

        form = PostForm()

    return render(
        request,
        'user/create_post.html',
        {
            'form': form
        }
    )

@login_required
def my_posts(request):

    posts = Post.objects.filter(
        author=request.user
    )

    return render(
        request,
        'user/my_posts.html',
        {'posts': posts}
    )

@login_required
def my_drafts(request):
    drafts = Post.objects.filter(
        author=request.user,
        status='draft'
    ).order_by('-created_at')

    return render(
        request,
        'user/my_drafts.html',
        {'drafts': drafts}
    )

from django.shortcuts import render, redirect, get_object_or_404

@login_required
def edit_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user
    )

    if request.method == 'POST':

        form = PostForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid():

            post = form.save(commit=False)

            if 'publish' in request.POST:
                post.status = 'published'
            elif 'draft' in request.POST:
                post.status = 'draft'

            post.save()

            form.save_m2m()

            messages.success(
                request,
                'Post updated successfully!'
            )

            return redirect('my_posts')

    else:

        form = PostForm(instance=post)

    return render(
        request,
        'user/edit_post.html',
        {
            'form': form,
            'post': post
        }
    )

@login_required
def delete_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user
    )

    if request.method == 'POST':

        post.delete()

        messages.success(
            request,
            'Post deleted successfully!'
        )

        return redirect('my_posts')

    return render(
        request,
        'user/delete_post.html',
        {
            'post': post
        }
    )

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Post, Like

@login_required
def toggle_like(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        status='published'
    )

    like = Like.objects.filter(
        post=post,
        user=request.user
    ).first()

    if like:
        
        like.delete()

    else:
       
        Like.objects.create(
            post=post,
            user=request.user
        )

    return redirect(
        request.META.get(
            'HTTP_REFERER',
            'blog_feed'
        )
    )

@login_required
def add_comment(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        status='published'
    )

    if request.method == 'POST':

        content = request.POST.get('content', '').strip()

        if content:
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )

            messages.success(
                request,
                'Comment added successfully!'
            )

        else:
            messages.error(
                request,
                'Comment cannot be empty.'
            )

    return redirect(
        request.META.get(
            'HTTP_REFERER',
            'blog_feed'
        )
    )

@login_required
def delete_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id
    )

    post = comment.post

    

    can_delete = (
        comment.user == request.user
        or post.author == request.user
        or request.user.is_staff
    )

    if not can_delete:
        messages.error(
            request,
            'You do not have permission to delete this comment.'
        )

        return redirect('blog_feed')

    if request.method == 'POST':

        comment.delete()

        messages.success(
            request,
            'Comment deleted successfully!'
        )

    return redirect('blog_feed')

@login_required
def post_detail(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug,
        status='published'
    )

    return render(
        request,
        'user/post_detail.html',
        {
            'post': post
        }
    )

@login_required
def profile(request):

    user_posts = Post.objects.filter(
        author=request.user
    )

    context = {
        'total_posts': user_posts.count(),

        'total_likes': Like.objects.filter(
            post__author=request.user
        ).count(),

        'total_comments': Comment.objects.filter(
            post__author=request.user
        ).count(),
    }

    return render(
        request,
        'user/profile.html',
        context
    )

@login_required
def edit_profile(request):

    if request.method == 'POST':

        form = EditProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Profile updated successfully!'
            )

            return redirect('profile')

    else:

        form = EditProfileForm(
            instance=request.user
        )

    return render(
        request,
        'user/edit_profile.html',
        {
            'form': form
        }
    )

@login_required
def change_password(request):

    if request.method == 'POST':

        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                'Your password has been changed successfully!'
            )

            return redirect('profile')

    else:

        form = PasswordChangeForm(
            request.user
        )

    return render(
        request,
        'user/change_password.html',
        {
            'form': form
        }
    )