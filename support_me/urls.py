"""support_me URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from core import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('core/', views.home, name='home'),
    path('admin/', admin.site.urls),
    # allauth account
    path('accounts/', include('allauth.urls')),
    path('brafitting/', views.braFitting, name='brafitting'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('bra-care/', views.BraCare, name='bra-care'),
    path('brafitting/suggestion-form/<int:fitting_id>', views.suggestion_form, name='suggestion-form'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
