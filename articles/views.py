from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from articles.models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article: Article = self.get_object()  # type: ignore[assignment]
        context['total_likes'] = article.total_likes()
        if self.request.user.is_authenticated:
            context['user_has_liked'] = article.likes.filter(
                pk=self.request.user.pk
            ).exists()
        else:
            context['user_has_liked'] = False
        return context


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['title', 'summary', 'body', 'photo']
    template_name = 'article_edit.html'

    def test_func(self):
        article: Article = self.get_object()  # type: ignore[assignment]
        return article.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        article: Article = self.get_object()  # type: ignore[assignment]
        return article.author == self.request.user


class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ['title', 'summary', 'body', 'photo']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser


@login_required
def like_article(request, pk):
    """Toggle like/unlike on an article (M2M relationship)."""
    article = get_object_or_404(Article, pk=pk)
    if article.likes.filter(pk=request.user.pk).exists():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    next_url = request.META.get('HTTP_REFERER', reverse('article_detail', args=[str(pk)]))
    return redirect(next_url)
