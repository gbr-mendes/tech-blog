"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from api import views

urlpatterns = [
    #  Django urls
    path('admin/', admin.site.urls),
    # Third party urls
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('accounts/', include('allauth.urls'), name='socialaccount_signup'),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/registration/register/', views.RegisterUserView.as_view(), name="rest_auth_register"),
    path('rest-auth/google/', views.GoogleLogin.as_view(), name='google_login'),
    #  Local urls
    path("", include("blog.urls")),
    path("api/", include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
