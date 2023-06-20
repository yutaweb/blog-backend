from django import forms
from blog.models import Comment, Article


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'comment',
        )


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
