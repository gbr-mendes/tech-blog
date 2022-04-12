from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path('posts', views.RetriveCreatePostsAPIView.as_view(), name="posts"),
    path('comments', views.ListCreateCommentAPIView.as_view(), name="comments"),
    path('send-email', views.EmailAPIView.as_view(), name='send_email')
]
