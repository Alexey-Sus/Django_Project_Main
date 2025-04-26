from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'short_descr', 'created_at',
                    'is_published')
    list_filter = ('title', 'is_published', 'created_at')
    search_fields = ('title', 'short_descr', 'content')
    ordering = ('created_at',)
    fields = ('title', 'short_descr', 'content', 'preview',
              'is_published', 'number_of_views')
    readonly_fields = ('created_at', 'updated_at')


