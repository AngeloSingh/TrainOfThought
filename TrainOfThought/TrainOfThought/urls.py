"""
URL configuration for TrainOfThought project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from backend import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('gpt-post/', views.gpt_post, name='gpt-post'),
    path('create_post/', views.create_post, name='create_post'),
    path('homepage/', views.homepage, name='homepage'),
    path('select_creator/', views.select_creator, name='select_creator'),
    path('get_posts/', views.get_posts, name='get_posts'),
    path('update_post/<int:post_id>/', views.update_post, name='update_post'),
    path('get_x_posts/', views.get_x_posts, name='get_x_posts')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
