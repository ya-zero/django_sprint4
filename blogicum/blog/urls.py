from django.urls import path
#from blog.views import category_posts, index, post_detail, PostCreateView, get_profile, edit_profile
from blog import views


app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    #path('profile/<slug:username>/edit/', edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.get_profile, name='profile'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    path('edit_profile/', views.ProfileUpdateView.as_view(),
         name='edit_profile'),
    path('category/', views.PostCreateView.as_view(),
         name='create_post'),
    path('posts/<int:post_id>/comment/', views.CommentCreateView.as_view(),
         name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.CommentUpdateView.as_view(),
         name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.CommentDeleteView.as_view(),
         name='delete_comment')
]
