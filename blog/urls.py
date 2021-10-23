"""blog URL Configuration

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
from django.urls import path,include
from django.contrib.sitemaps.views import sitemap
from blog_app.sitemaps import PostSiteMap
from django.conf import settings
from django.conf.urls.static import static
from blog_app import views as post


sitemaps = {
    'posts':PostSiteMap,
}

urlpatterns = [
    path('admin/blog_app/post/add/', post.CreatePost.as_view()),
    path('admin/blog_app/post/<int:pk>/change/', post.CreatePost.as_view()),
    path('admin/', admin.site.urls),
    path('',include('blog_app.urls',namespace='blog_app')),
    path('sitemap.xml',sitemap,{'sitemaps':sitemaps},name='django.contrib.sitemaps.views.sitemap'),
    path('summernote/',include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
