from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from blog.apps import NewappConfig
from blog.views import (ArticleCreateView, ArticleDetailView, BaseArticleListView,
                        ArticleListView, ArticleUpdateView, ArticleDeleteView)
app_name = NewappConfig.name

urlpatterns = [
    path('article_list/', ArticleListView.as_view(), name='article_list'),
    path('base_article_template/', BaseArticleListView.as_view(), name='base_template'),
    path('article_form/<int:pk>/', ArticleDetailView.as_view(), name='article_form'),
    path('article_form_create/', ArticleCreateView.as_view(), name='article_form_create'),
    path('article_update/<int:pk>/update/', ArticleUpdateView.as_view(), name='article_update'),
    path('article_delete/<int:pk>/', ArticleDeleteView.as_view(), name='article_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
