from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import (
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
from django.views.generic.edit import CreateView

from blog.constant import POST_PER_PAGE
from blog.forms import CommentForm, PostForm
from blog.mixin import CommentMixin, OnlyAuthorMixin
from blog.models import Category, Post
from blog.service import get_base_request


def category_posts(request, category_slug):
    category = get_object_or_404(Category.objects.filter(is_published=True),
                                 slug=category_slug)
    posts = (
        get_base_request()
        .filter(category=category)
        .annotate(comment_count=Count("comments"))
    )
    paginator = Paginator(posts, POST_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category.html',
                  {'category': category, 'page_obj': page_obj})


class IndexList(ListView):
    template_name = 'blog/index.html'
    paginate_by = POST_PER_PAGE
    model = Post
    queryset = get_base_request()

    def get_queryset(self):
        return self.queryset.annotate(comment_count=Count('comments'))


class PostDetail(DetailView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context

    def get_object(self):
        obj = super().get_object()
        if obj.author == self.request.user:
            return obj
        return get_object_or_404(get_base_request(), pk=self.kwargs['post_id'])


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user})


class PostEdit(LoginRequiredMixin, OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class PostDeleteView(LoginRequiredMixin, OnlyAuthorMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.get_object())
        return context

    def get_success_url(self):
        return reverse('blog:index')


class CommentCreateView(LoginRequiredMixin, CommentMixin, CreateView):
    form_class = CommentForm

    def form_valid(self, form,):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin,
                        OnlyAuthorMixin,
                        CommentMixin,
                        UpdateView):
    form_class = CommentForm


class CommentDeleteView(LoginRequiredMixin,
                        OnlyAuthorMixin,
                        CommentMixin,
                        DeleteView):
    pass


class GetProfile(ListView):
    template_name = 'blog/profile.html'
    model = Post
    paginate_by = POST_PER_PAGE

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user == user:
            return (
                Post.objects.filter(author=user)
                .annotate(comment_count=Count("comments"))
                .order_by("-pub_date")
                .select_related("category", "author", "location")
            )
        return (
            get_base_request()
            .filter(
                author=user,
            )
            .annotate(comment_count=Count("comments"))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['profile'] = get_object_or_404(User, username=username)
        return context


class EditProfile(LoginRequiredMixin, UpdateView):
    template_name = 'blog/user.html'
    model = User
    fields = ('username', 'email', 'first_name', 'last_name')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        username = self.request.user.username
        return reverse('blog:profile', kwargs={'username': username})
