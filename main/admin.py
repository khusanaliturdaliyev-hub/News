from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Article, Context, Comment, Newsletter


# --- 1. Inlines ---
class ContextInline(admin.StackedInline):
    model = Context
    extra = 1

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


# --- 2. Admin Classes ---

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # 'is_motivation' maydonini ro'yxatga qo'shdik, shunda admin paneldan ajratib olsa bo'ladi
    list_display = ('title', 'is_motivation', 'cover_preview', 'author', 'category', 'published', 'important', 'created_at')
    list_filter = ('is_motivation', 'published', 'author', 'category', 'important')
    search_fields = ('title', 'intro')
    inlines = [ContextInline, CommentInline]
    prepopulated_fields = {'slug': ('title',)}

    def cover_preview(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" width="100" height="60" style="object-fit:cover; border-radius:5px;" />',
                obj.cover.url
            )
        return "Rasm yo‘q"
    cover_preview.short_description = "Muqova"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'name', 'email', 'created_at')
    list_filter = ('created_at',)

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')

# Agar kerak bo'lsa boshqa modellarni ham register qilishingiz mumkin
# admin.site.register(Moment)
# admin.site.register(Contact)