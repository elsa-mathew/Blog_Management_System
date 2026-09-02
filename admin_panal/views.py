from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from blog.forms import CategoryForm, PostForm
from blog.models import Post, Comment, Like, Category
from django.contrib.auth import authenticate, login
from blog.models import Post, Comment, Like, Category, Tag
from blog.forms import PostForm, CategoryForm, TagForm


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('login')

        if not request.user.is_staff:
            messages.error(
                request,
                'You do not have permission to access the admin panel.'
            )
            return redirect('blog_feed')

        return view_func(request, *args, **kwargs)

    return wrapper


@admin_required
def admin_dashboard(request):

    context = {

        'total_users': User.objects.count(),

        'total_posts': Post.objects.count(),

        'published_posts': Post.objects.filter(
            status='published'
        ).count(),

        'draft_posts': Post.objects.filter(
            status='draft'
        ).count(),

        'total_comments': Comment.objects.count(),

        'total_likes': Like.objects.count(),

        'recent_posts': Post.objects.select_related(
            'author'
        ).order_by('-created_at')[:5],

        'recent_users': User.objects.order_by(
            '-date_joined'
        )[:5],
    }

    return render(
        request,
        'admin/admin_dashboard.html',
        context
    )



@admin_required
def admin_users(request):

    search_query = request.GET.get(
        'q',
        ''
    ).strip()

    users = User.objects.all().order_by(
        '-date_joined'
    )

    if search_query:

        users = users.filter(
            Q(username__icontains=search_query)
            | Q(email__icontains=search_query)
        )

    return render(
        request,
        'admin/users.html',
        {
            'users': users,
            'search_query': search_query,
        }
    )



@admin_required
def admin_user_detail(request, user_id):

    selected_user = get_object_or_404(
        User,
        id=user_id
    )

    user_posts = Post.objects.filter(
        author=selected_user
    )

    context = {
        'selected_user': selected_user,

        'user_posts': user_posts,

        'total_posts': user_posts.count(),

        'total_likes': Like.objects.filter(
            post__author=selected_user
        ).count(),

        'total_comments': Comment.objects.filter(
            post__author=selected_user
        ).count(),
    }

    return render(
        request,
        'admin/user_detail.html',
        context
    )


@admin_required
def toggle_user_status(request, user_id):

    selected_user = get_object_or_404(
        User,
        id=user_id
    )

    if selected_user == request.user:

        messages.error(
            request,
            'You cannot deactivate your own account.'
        )

        return redirect(
            'admin_user_detail',
            user_id=user_id
        )

    if request.method == 'POST':

        selected_user.is_active = not selected_user.is_active

        selected_user.save(
            update_fields=['is_active']
        )

        if selected_user.is_active:

            messages.success(
                request,
                f'{selected_user.username} has been activated.'
            )

        else:

            messages.success(
                request,
                f'{selected_user.username} has been deactivated.'
            )

    return redirect(
        'admin_user_detail',
        user_id=user_id
    )


@admin_required
def delete_user(request, user_id):

    selected_user = get_object_or_404(
        User,
        id=user_id
    )

    if selected_user == request.user:

        messages.error(
            request,
            'You cannot delete your own admin account.'
        )

        return redirect(
            'admin_user_detail',
            user_id=user_id
        )

    if request.method == 'POST':

        username = selected_user.username

        selected_user.delete()

        messages.success(
            request,
            f'User "{username}" has been deleted successfully.'
        )

        return redirect('admin_users')

    return redirect(
        'admin_user_detail',
        user_id=user_id
    )

@admin_required
def admin_posts(request):

    search_query = request.GET.get(
        'q',
        ''
    ).strip()

    status_filter = request.GET.get(
        'status',
        ''
    ).strip()

    posts = Post.objects.select_related(
        'author',
        'category'
    ).prefetch_related(
        'tags'
    ).order_by(
        '-created_at'
    )


    if search_query:

        posts = posts.filter(
            Q(title__icontains=search_query)
            | Q(author__username__icontains=search_query)
        )


    if status_filter in ['published', 'draft']:

        posts = posts.filter(
            status=status_filter
        )


    return render(
        request,
        'admin/posts.html',
        {
            'posts': posts,
            'search_query': search_query,
            'status_filter': status_filter,
        }
    )
 
@admin_required
def admin_post_detail(request, post_id):

    post = get_object_or_404(
        Post.objects.select_related(
            'author',
            'category'
        ).prefetch_related(
            'tags'
        ),
        id=post_id
    )

    return render(
        request,
        'admin/post_detail.html',
        {
            'post': post
        }
    )

@admin_required
def admin_edit_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id
    )

    if request.method == 'POST':

        form = PostForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Post updated successfully!'
            )

            return redirect(
                'admin_post_detail',
                post_id=post.id
            )

    else:

        form = PostForm(
            instance=post
        )

    return render(
        request,
        'admin/edit_post.html',
        {
            'form': form,
            'post': post
        }
    )

@admin_required
def admin_delete_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id
    )

    if request.method == 'POST':

        title = post.title

        post.delete()

        messages.success(
            request,
            f'Post "{title}" deleted successfully.'
        )

        return redirect('admin_posts')

    return redirect(
        'admin_post_detail',
        post_id=post_id
    )

@admin_required
def admin_toggle_post_status(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id
    )

    if request.method == 'POST':

        if post.status == 'published':

            post.status = 'draft'

            message = 'Post moved to draft.'

        else:

            post.status = 'published'

            message = 'Post published successfully.'

        post.save(
            update_fields=['status']
        )

        messages.success(
            request,
            message
        )

    return redirect(
        'admin_post_detail',
        post_id=post_id
    )

@admin_required
def admin_categories(request):

    search_query = request.GET.get(
        'q',
        ''
    ).strip()

    categories = Category.objects.all().order_by(
        'name'
    )

    if search_query:

        categories = categories.filter(
            name__icontains=search_query
        )

    return render(
        request,
        'admin/categories.html',
        {
            'categories': categories,
            'search_query': search_query,
        }
    )
@admin_required
def admin_create_category(request):

    if request.method == 'POST':

        form = CategoryForm(
            request.POST
        )

        if form.is_valid():

            category = form.save()

            messages.success(
                request,
                f'Category "{category.name}" created successfully.'
            )

            return redirect('admin_categories')

    else:

        form = CategoryForm()

    return render(
        request,
        'admin/category_form.html',
        {
            'form': form,
        }
    )
@admin_required
def admin_edit_category(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id
    )

    if request.method == 'POST':

        form = CategoryForm(
            request.POST,
            instance=category
        )

        if form.is_valid():

            category = form.save()

            messages.success(
                request,
                f'Category "{category.name}" updated successfully.'
            )

            return redirect('admin_categories')

    else:

        form = CategoryForm(
            instance=category
        )

    return render(
        request,
        'admin/category_form.html',
        {
            'form': form,
            'category': category,
        }
    )

@admin_required
def admin_delete_category(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id
    )

    if request.method == 'POST':

        category_name = category.name

        category.delete()

        messages.success(
            request,
            f'Category "{category_name}" deleted successfully.'
        )

    return redirect('admin_categories')

@admin_required
def admin_tags(request):
    search_query = request.GET.get('q', '').strip()

    tags = Tag.objects.all().order_by('name')

    if search_query:
        tags = tags.filter(
            name__icontains=search_query
        )

    return render(request, 'admin/tags.html', {
        'tags': tags,
        'search_query': search_query,
    })


@admin_required
def admin_create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)

        if form.is_valid():
            tag = form.save()

            messages.success(
                request,
                f'Tag "{tag.name}" created successfully.'
            )

            return redirect('admin_tags')

    else:
        form = TagForm()

    return render(request, 'admin/tag_form.html', {
        'form': form
    })


@admin_required
def admin_edit_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)

    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)

        if form.is_valid():
            tag = form.save()

            messages.success(
                request,
                f'Tag "{tag.name}" updated successfully.'
            )

            return redirect('admin_tags')

    else:
        form = TagForm(instance=tag)

    return render(request, 'admin/tag_form.html', {
        'form': form,
        'tag': tag
    })


@admin_required
def admin_delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)

    if request.method == 'POST':
        tag_name = tag.name
        tag.delete()

        messages.success(
            request,
            f'Tag "{tag_name}" deleted successfully.'
        )

    return redirect('admin_tags')

@admin_required
def admin_comments(request):

    search_query = request.GET.get('q', '').strip()

    comments = Comment.objects.select_related(
        'user',
        'post'
    ).order_by('-created_at')

    if search_query:
        comments = comments.filter(
            Q(content__icontains=search_query)
            | Q(user__username__icontains=search_query)
            | Q(post__title__icontains=search_query)
        )

    return render(request, 'admin/comments.html', {
        'comments': comments,
        'search_query': search_query,
    })


@admin_required
def admin_delete_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id
    )

    if request.method == 'POST':

        comment.delete()

        messages.success(
            request,
            'Comment deleted successfully.'
        )

    return redirect('admin_comments')