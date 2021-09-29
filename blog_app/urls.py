from django.urls import path
from . import views
from .feeds import LatestPostFeed
app_name = 'blog_app'

urlpatterns =[
    path('',views.PostListView.as_view(),name='post_list'),
    path('tag/<slug:tag_slug>/',views.PostListView.as_view(),name='post_list_by_tag'),
    path('<int:pk>/',views.PostDetailView.as_view(),name='post_detail'),
    path('latest/',views.PostDetailView.as_view(),name='latest_post_detail'),
    path('<int:pk>/share',views.post_share,name='post_share'),
    path('feed/',LatestPostFeed(),name='post_feed'),
    path('about/',views.AboutView.as_view(),name='about_page'),
    path('contact/',views.ContactView.as_view(),name='contact_page')
]
