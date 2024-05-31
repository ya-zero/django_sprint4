from django.shortcuts import get_object_or_404, render

from blog.constant import COUNT_POST
from blog.models import Category, Post, User, Comment
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View)
from .forms import CommentForm, PostForm

def get_base_request():
    current_date = timezone.now()
    return (
        Post.objects.select_related("category", "author", "location")
        .filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=current_date
        )
        .order_by("pub_date")
    )


def index(request):
    posts = get_base_request()[:COUNT_POST]
    return render(request, 'blog/index.html', {'post_list': posts})


def post_detail(request, post_id):
    post = get_object_or_404(get_base_request(),
                             pk=post_id)
    return render(request, 'blog/detail.html',
                  {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(Category.objects.filter(is_published=True),
                                 slug=category_slug)
    posts = get_base_request().filter(category=category)
    return render(request, 'blog/category.html',
                  {'category': category, 'post_list': posts})


class PostCreateView(CreateView):
    model = Post
    fields = '__all__'
    template_name = 'blog/index.html'
    success_url = reverse_lazy('blog:index')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = ('username', 'first_name', 'last_name', 'email')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )




def get_profile(request, username):
    profile = get_object_or_404(User, username=username)
    #user_posts = Post.objects.filter(author=profile.).order_by(
    #    '-pub_date')
    #paginator = Paginator(user_posts, 10)
    #page_number = request.GET.get('page')
    #page_obj = paginator.get_page(page_number)

    context = {
        'profile': profile,
        #'page_obj': page_obj,
        }
    return render(request, 'blog/profile.html', context)

class CommentMixin(LoginRequiredMixin):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['post_id']])

    def dispatch(self, request, *args, **kwargs):
        coment = get_object_or_404(Comment, id=self.kwargs['comment_id'])
        if coment.author != self.request.user:
            return redirect('blog:post_detail',
                            post_id=self.kwargs['post_id']
                            )
        return super().dispatch(request, *args, **kwargs)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        return dict(**super().get_context_data(**kwargs), form=CommentForm())

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['post_id']])


class CommentUpdateView(CommentMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(CommentMixin, DeleteView):
    pass
