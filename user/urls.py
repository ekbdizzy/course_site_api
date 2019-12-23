from django.urls import path
from .views import CreateUserView, AuthenticateUserView
from django.contrib.auth.views import LogoutView

app_name = 'user'

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('login/', AuthenticateUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='user:login'), name='logout'),
]
