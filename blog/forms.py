from django import forms
from blog.models import Comment, Article


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'comment',
        )


class ArticleForm(forms.ModelForm):
    # viewsの中でget_formメソッドで変更する事も可能
    # https://yu-nix.com/archives/django-create-view/
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'タイトル'
        self.fields['text'].label = '本文'
        self.fields['image'].label = '画像'
        self.fields['author'].label = '投稿者'
        self.fields['tags'].label = 'タグ'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Article
        fields = (
            'title',
            'text',
            'image',
            'author',
            'tags'
        )
