from django.contrib import admin
from .models import Article, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    filter_horizontal = ('likes',)
    list_display = ('title', 'author', 'date', 'total_likes')
    list_filter = ('date',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
