from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('user/register/', views.RegistrationView.as_view(), name='register'),
    path('user/login/', views.LoginUserView.as_view(), name='login'),
    path('user/logout/', views.LogoutView.as_view(), name='logout'),
    path('user/avatar/', views.UserAvatarUpload.as_view(), name='avatar'),
    path('user/profile/update/', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('user/password/update/', views.ChangePasswordView.as_view(), name='password-update'),
    path('user/post/', views.PostCreateAPIView.as_view(), name='post'),
    path('user/like/post/', views.LikePostCreateAPIView.as_view(), name='like_post'),
    path('user/unlike/post/', views.UnLikePostCreateAPIView.as_view(), name='unlike_post'),
    path('user/follow/', views.FollowUserAPIView.as_view(), name='user_follow'),
]
