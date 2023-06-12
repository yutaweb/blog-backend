from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Article, Comment, Tag
from django.core.paginator import Paginator
from blog.forms import CommentForm
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.views.generic import ListView, DetailView


class IndexView(ListView):
    model = Article
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['page_title'] = '記事一覧'
        return context_data


class ArticleView(DetailView):
    model = Article
    # queryset = Article.objects.all()  # model = Articleと同義

    def get_context_data(self, **kwargs):
        # getをオーバーライドしてrenderしても良い
        context = super().get_context_data(**kwargs)
        context['is_already_exist'] = self.request.user not in self.object.users.all()
        context['comments'] = Comment.objects.filter(article=self.object)
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('like_count', None):  # 取得失敗にNone
            request.count += 1
            request.save()
        else:
            form = CommentForm(request.POST or None)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.article = Article.objects.get(pk=self.kwargs['pk'])
                comment.save()
        return redirect('blog:detail', self.kwargs['pk'])


def tags(request, slug):
    tag = Tag.objects.get(slug=slug)
    objs = tag.article_set.all()  # tagを参照しているartickeを逆参照で取得

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('page')
    context = {
        'page_title': '記事一覧 #{}'.format(slug),
        'page_obj': paginator.get_page(page_number),
        'page_number': page_number,
    }
    return render(request, 'blog/blogs.html', context)


@ensure_csrf_cookie
def like(request, pk):
    d = {"message": "error"}
    if request.method == 'POST':
        obj = Article.objects.get(pk=pk)
        if request.user.is_authenticated and request.user not in obj.users.all():
            obj.users.add(request.user)
            obj.count += 1
            obj.save()

            d["message"] = "success"
    return JsonResponse(d)
