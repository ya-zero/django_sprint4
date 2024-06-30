from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from blog.models import Comment


class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        return redirect(reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        ))


class CommentMixin:
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )
    # выполняет одинаковое действие.
    # def get_success_url(self):
    #     return reverse(
    #         'blog:post_detail',
    #         kwargs={'post_id': self.object.post.pk}
    #     )
