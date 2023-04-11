from django.urls import path

from .views import *

app_name = 'blog'

urlpatterns=[
    path('d/<str:slug>/', PostDetail.as_view(), name='post_detail'),
    path('add/',NewBlogView.as_view(),name="post_add"),
    path('edit/<int:pk>/',UpdateBlogPostView.as_view(),name="post_update"),
    path('', post_list, name='post_list'),
    path('delete/<int:pk>/',DeletePost.as_view(),name="post_delete"),

    path('comment/reply/', reply_page, name="reply"), 
    
    path('tag/<slug:tag_slug>/',post_list, name='post_tag'),

    path('thumbs/', thumbs, name='thumbs'),
]