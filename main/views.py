from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from datetime import datetime
from .models import Article, Category, Newsletter, Comment, Contact


def home_view(request):
    main_articles = Article.objects.select_related('category').filter(published=True).exclude(slug__in=['', None]).order_by('-important', '-views')[
        :9]
    latest_articles = Article.objects.select_related('category').filter(published=True).exclude(slug__in=['', None]).order_by('-created_at')[:8]

    categories = Category.objects.all()
    category_articles = {}

    for category in categories:
        articles = Article.objects.filter(published=True, category=category).exclude(slug__in=['', None]).order_by('-created_at')
        if articles.exists():
            category_articles[category.id] = {
                'category': category,
                'main_article': articles.first(),
                'side_articles': articles[1:5] if articles.count() > 1 else []
            }

    most_viewed_articles = Article.objects.filter(published=True).exclude(slug__in=['', None]).order_by('-views')[:5]

    # Motivatsiya bo'limi uchun ma'lumotlar
    motivation_all = Article.objects.filter(published=True, is_motivation=True).exclude(slug__in=['', None]).order_by('-id')
    motivation_main = motivation_all.first()
    motivation_list = motivation_all[1:4]

    context = {
        'main_articles': main_articles,
        'latest_articles': latest_articles,
        'category_articles': category_articles,
        'most_viewed_articles': most_viewed_articles,
        'motivation_main': motivation_main,
        'motivation_list': motivation_list,
        'today': datetime.today(),
    }
    return render(request, 'index.html', context)


class ArticleDetailView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug, published=True)
        article.views += 1
        article.save(update_fields=['views'])

        like_articles = Article.objects.select_related('category').filter(
            published=True,
            category=article.category
        ).exclude(slug=slug).exclude(slug__in=['', None]).order_by('-created_at')[:4]

        # Tafsilotlar sahifasi uchun ham motivatsiya postlarini olish
        motivation_all = Article.objects.filter(published=True, is_motivation=True).exclude(slug__in=['', None]).order_by('-id')
        motivation_main = motivation_all.first()
        motivation_list = motivation_all[1:4]

        context = {
            'article': article,
            'like_articles': like_articles,
            'motivation_main': motivation_main,
            'motivation_list': motivation_list,
        }
        return render(request, 'article-details.html', context)

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug, published=True)
        name = request.POST.get('name')
        email = request.POST.get('email')
        text = request.POST.get('text')

        if text:
            Comment.objects.create(
                name=name or "Anonim",
                email=email or "",
                text=text,
                article=article,
            )
        return redirect('article-details', slug=slug)


class CategoryDetailsView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        articles = category.article_set.filter(published=True).exclude(slug__in=['', None]).order_by('-created_at')
        context = {
            'category': category,
            'articles': articles,
        }
        return render(request, 'category-details.html', context)


class NewsletterCreateView(View):
    def post(self, request):
        email = request.POST.get('email')
        if email:
            Newsletter.objects.get_or_create(email=email)
        return redirect('home')

class MotivatsiyaDetailsView(ArticleDetailView):
    pass

class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        if name and subject:
            try:
                contact = Contact(name=name, email=email, subject=subject, message=message)
                contact.full_clean()
                contact.save()
            except Exception:
                pass
        return redirect('contact')