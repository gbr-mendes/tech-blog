from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path('posts/', views.RetrivePostsAPIView.as_view(), name="posts"),
    path('send-email/', views.EmailAPIView.as_view(), name='send_email')
]
