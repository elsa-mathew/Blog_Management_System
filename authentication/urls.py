from django.urls import path
from .views import forgot_password, home_page, login_page, logout_view, register_page

urlpatterns = [
    path('', login_page, name='login'), 
    path('register/', register_page, name='register'), 
    path('forgot-password/', forgot_password, name='forgot_password'),  
    path('home/', home_page, name='home'),
    path('logout/', logout_view, name='logout'),
]