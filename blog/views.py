from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from blog.models import Article
from django.urls import *


class BaseArticleListView(ListView):
    model = Article
    template_name = 'base_article_template.html'


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(is_published=True)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_form.html'

    def get_object(self):
        obj = super().get_object()
        obj.number_of_views += 1
        obj.save()
        return obj

class ArticleCreateView(CreateView):
    model = Article
    fields = ('title', 'short_descr', 'content', 'preview', 'is_published', 'number_of_views')
    template_name = 'article_form_create.html'
    success_url = reverse_lazy('blog:article_list')


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ('title', 'short_descr', 'content', 'preview', 'is_published')
    template_name = 'article_update.html'

    def get_success_url(self):
        return reverse('blog:article_form', kwargs={'pk': self.object.pk})


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('blog:article_list')
