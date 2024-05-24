from django.urls import path

from blog.views import category_posts, index, post_detail,PostCreateView, handle_url_error

app_name = 'blog'


urlpatterns = [
    path('', index, name='index'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', category_posts,
         name='category_posts'),
    path('category/', PostCreateView.as_view(),
         name='create_post'),
    path('category/', handle_url_error,
         name='profile'),
]
