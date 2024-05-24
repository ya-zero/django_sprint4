from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.http import HttpResponseNotFound
from blog.constant import COUNT_POST
from blog.models import Category, Post
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

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
    # Указываем модель, с которой работает CBV...
    model = Post
    # Этот класс сам может создать форму на основе модели!
    # Нет необходимости отдельно создавать форму через ModelForm.
    # Указываем поля, которые должны быть в форме:
    fields = '__all__'
    # Явным образом указываем шаблон:
    template_name = 'blog/index.html'
    # Указываем namespace:name страницы, куда будет перенаправлен пользователь
    # после создания объекта:
    success_url = reverse_lazy('blog:index')

def handle_url_error(request, exception):
    return HttpResponseNotFound("Страница не найдена. Здесь может быть ваша заглушка для ошибки.")
