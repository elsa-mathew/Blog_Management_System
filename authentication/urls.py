from django.urls import path

from .views import forgot_password, login_page, logout_view, register_page
from blog.views import blog_feed


urlpatterns = [

    path('', login_page, name='login'),

    path('register/', register_page, name='register'),

    path('forgot-password/', forgot_password, name='forgot_password'),

    path('home/', blog_feed, name='home'),

    path('logout/', logout_view, name='logout'),

]