from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path('create/', views.CreateUserAPIView.as_view(), name="create_user"),
    path('token/', views.CreateTokenView.as_view(), name='token_user'),
    path('me/', views.ManagerUserView.as_view(), name='me'),
    path('posts/', views.RetrivePostsAPIView.as_view(), name="posts"),
]
