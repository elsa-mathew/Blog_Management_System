from django.urls import path
from . import views 

urlpatterns = [

    path(
        'dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
    'users/',
    views.admin_users,
    name='admin_users'
),

path(
    'users/<int:user_id>/',
    views.admin_user_detail,
    name='admin_user_detail'
),
path(
    'users/<int:user_id>/toggle-status/',
    views.toggle_user_status,
    name='toggle_user_status'
),

path(
    'users/<int:user_id>/delete/',
    views.delete_user,
    name='delete_user'
),
path(
    'posts/',
    views.admin_posts,
    name='admin_posts'
),
path(
    'posts/<int:post_id>/',
    views.admin_post_detail,
    name='admin_post_detail'
),
path(
    'posts/<int:post_id>/edit/',
    views.admin_edit_post,
    name='admin_edit_post'
),
path(
    'posts/<int:post_id>/delete/',
    views.admin_delete_post,
    name='admin_delete_post'
),
path(
    'posts/<int:post_id>/toggle-status/',
    views.admin_toggle_post_status,
    name='admin_toggle_post_status'
),
path(
    'categories/',
    views.admin_categories,
    name='admin_categories'
),
path(
    'categories/create/',
    views.admin_create_category,
    name='admin_create_category'
),
path(
    'categories/<int:category_id>/edit/',
    views.admin_edit_category,
    name='admin_edit_category'
),
path(
    'categories/<int:category_id>/delete/',
    views.admin_delete_category,
    name='admin_delete_category'
),
path(
    'tags/',
    views.admin_tags,
    name='admin_tags'
),

path(
    'tags/create/',
    views.admin_create_tag,
    name='admin_create_tag'
),

path(
    'tags/<int:tag_id>/edit/',
    views.admin_edit_tag,
    name='admin_edit_tag'
),

path(
    'tags/<int:tag_id>/delete/',
    views.admin_delete_tag,
    name='admin_delete_tag'
),
path(
    'comments/',
    views.admin_comments,
    name='admin_comments'
),

path(
    'comments/<int:comment_id>/delete/',
    views.admin_delete_comment,
    name='admin_delete_comment'
),
]