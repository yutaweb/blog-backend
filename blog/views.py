from django.shortcuts import redirect
from blog.models import Article, Comment, Tag
from blog.forms import ArticleForm, CommentForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views import View
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from functools import reduce
from operator import and_


class IndexView(ListView):
    model = Article
    paginate_by = 3
    queryset = Article.objects.order_by('-created_at')

    def get_queryset(self):
        # self.object, self.kwargs
        # https://qiita.com/keishi04hrikzira/items/3e07cffa247895f841a0
        queryset = Article.objects.order_by('-created_at')
        query = self.request.GET.get('query')
        if query:
            exclusion = set([' ', '　'])
            query_list = ''
            for i in query:
                if i in exclusion:
                    pass
                else:
                    query_list += i

            query = reduce(
                and_, [Q(title__icontains=q) | Q(text__icontains=q) for q in query_list]
            )
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['page_title'] = '記事一覧'
        context_data['query'] = self.request.GET.get('query')
        return context_data


class CreateArticleView(LoginRequiredMixin, CreateView):
    form_class = ArticleForm
    success_url = reverse_lazy('blog:list')
    template_name = 'blog/article_form.html'
    # 投稿ユーザを保存可能にする際にform_validを設ける。


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


class UpdateArticleView(UpdateView):
    model = Article
    form_class = ArticleForm

    def get_success_url(self):
        # https://stackoverflow.com/questions/59475392/success-url-from-updateview-to-detailview-with-pk-in-django#:~:text=You%20can%20use%20the%20get_success_url%20method%20in%20your,get_success_url%20%28self%29%3A%20return%20reverse_lazy%20%28%27account%3Agroup_detail%27%2C%20kwargs%3D%20%7B%27pk%27%3A%20self.object.pk%7D%29
        return reverse_lazy('blog:detail', kwargs={'pk': self.object.pk})


class DeleteArticleView(DeleteView):
    model = Article
    success_url = reverse_lazy('blog:list')


class Tags(ListView):
    model = Tag
    # queryset = Tag.article_set.all()
    template_name = 'blog/article_list.html'
    paginate_by = 10

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.get(slug=self.kwargs['slug'])
        queryset = queryset.article_set.all()
        # queryset = Tag.objects.get(slug=self.kwargs['slug']).article_set.all()
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['page_title'] = '記事一覧 #{}'.format(self.kwargs['slug'])
        return context_data


# View: get(), post()などHTTPメソッドに特化したビュー
# https://di-acc2.com/programming/python/5210/
class Like(View):
    
    d = {"message": "error"}

    def get(self, request):
        return JsonResponse(self.d)

    # https://code-examples.net/ja/q/1330d0b
    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        obj = Article.objects.get(pk=self.kwargs['pk'])
        if request.user.is_authenticated and request.user not in obj.users.all():
            obj.users.add(request.user)
            obj.count += 1
            obj.save()

            self.d["message"] = "success"
        return JsonResponse(self.d)
