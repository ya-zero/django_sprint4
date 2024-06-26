from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import DeleteView, DetailView, ListView, UpdateView
from django.views.generic.edit import CreateView

from blog.forms import CommentForm, PostForm
from blog.models import Category, Comment, Post


class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        return redirect(reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        ))


def get_base_request():
    current_date = timezone.now()
    return (
        Post.objects.select_related("category", "author", "location")
        .filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=current_date
        )
        .order_by("-pub_date")
    )


def category_posts(request, category_slug):
    category = get_object_or_404(Category.objects.filter(is_published=True),
                                 slug=category_slug)
    posts = get_base_request().filter(category=category)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category.html',
                  {'category': category, 'page_obj': page_obj})



class IndexList(ListView):
    template_name = 'blog/index.html'
    paginate_by = 10
    model = Post

    def get_queryset(self):
        return super().get_queryset().filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        ).annotate(comment_count=Count('comments')).order_by('-pub_date')


class PostDetail(DetailView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if not post.is_published and request.user != post.author:
            raise Http404("Эта запись не опубликована")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    # прописано в форме exclude = ('author',)

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user})


class PostEdit(OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class PostDelete(OnlyAuthorMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:index')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        self.post_odject = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_odject
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class CommentUpdateView(OnlyAuthorMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.pk}
        )


class CommentDeleteView(OnlyAuthorMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.pk}
        )


class GetProfile(ListView):
    template_name = 'blog/profile.html'
    model = Post
    ordering = '-pub_date'
    paginate_by = 10

    def get_queryset(self):
        username = self.kwargs['username']  # Получаем значение username из URL
        user = get_object_or_404(User, username=username)
        return (Post.objects.filter(author=user,).
                annotate(comment_count=Count('comments')).
                order_by('-pub_date'))

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста из родительского метода.
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['profile'] = get_object_or_404(User, username=username)
        # context['page_obj'] = Post.objects.filter(author__username=username)
        # .order_by('-pub_date')
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
        # Передача имени пользователя в success_url
