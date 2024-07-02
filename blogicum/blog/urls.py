from django.urls import path

from blog.views import (CommentCreateView, CommentDeleteView,
                        CommentUpdateView, CreatePost, EditProfile, GetProfile,
                        IndexList, PostDeleteView, PostDetail, PostEdit,
                        category_posts)

app_name = 'blog'

urlpatterns = [
    path('', IndexList.as_view(), name='index'),
    path('posts/<int:post_id>/', PostDetail.as_view(), name='post_detail'),
    path('posts/create/', CreatePost.as_view(), name='create_post'),
    path('posts/<int:post_id>/edit/', PostEdit.as_view(), name='edit_post'),
    path('posts/<int:post_id>/delete/',
         PostDeleteView.as_view(),
         name='delete_post'),
    path('category/<slug:category_slug>/', category_posts,
         name='category_posts'),
    path('profile/<str:username>/', GetProfile.as_view(), name='profile'),
    path('edit_profile/', EditProfile.as_view(), name='edit_profile'),
    path('posts/<int:post_id>/comment/',
         CommentCreateView.as_view(),
         name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         CommentUpdateView.as_view(),
         name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         CommentDeleteView.as_view(),
         name='delete_comment'),
]
