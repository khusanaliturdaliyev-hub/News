from django.contrib import admin
from django.urls import path

from django.conf.urls.static import static
from django.conf import settings

from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('newsletter-create/', NewsletterCreateView.as_view(), name='newsletter-create'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article-details'),
    path('category/<int:pk>/', CategoryDetailsView.as_view(), name='category-details'),
    # Mana shu qatorni qo'shing:
    path('motivation/<slug:slug>/', MotivatsiyaDetailsView.as_view(), name='motivation_page'),
    path('contact/', ContactView.as_view(), name='contact'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)