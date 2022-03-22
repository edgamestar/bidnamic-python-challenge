"""bidnamic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1.7/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

from bidnamic import base_settings
from portal import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('bidnamic/admin/', admin.site.urls),
    re_path(r'^bidnamic/auth/(?P<target>[-\w]+)/$', views.AuthenticationView.as_view(), name='auth'),
    path('bidnamic/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # drf simplejwt
    path('bidnamic/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # drf simplejwt
    re_path(r'^bidnamic/api/(?P<target>[-\w]+)/(?P<action>[-\w]+)/$', views.ApiView.as_view(), name='api'),
    re_path(r'^bidnamic(?:/(?P<target>[-\w]+)/(?P<action>[-\w]+))?/$', views.IndexView.as_view(), name='index'),
]

urlpatterns += static(base_settings.MEDIA_URL, document_root=base_settings.MEDIA_ROOT)
