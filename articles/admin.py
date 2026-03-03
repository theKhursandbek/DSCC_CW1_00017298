from django.contrib import admin
from .models import Article, Comment, Tag


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    filter_horizontal = ('tags',)
    list_display = ('title', 'author', 'date')
    list_filter = ('date', 'tags')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
