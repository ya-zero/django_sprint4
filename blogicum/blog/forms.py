from django import forms

from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class PostForm(forms.ModelForm):
    # код менял , так как писал с нулю, непонял тему
    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',
                                            attrs={'type': 'datetime-local'}),
            'text': forms.Textarea(attrs={'cols': 10, 'rows': 10})
        }
