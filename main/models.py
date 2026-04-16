from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self): return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self): return self.name


class Article(models.Model):
    title = models.CharField(max_length=255)
    # Motivatsiya maqolasi ekanligini belgilovchi maydon
    is_motivation = models.BooleanField(default=False)
    slug = models.SlugField(max_length=300, unique=True, blank=True, db_index=True)
    intro = models.TextField()
    cover = models.ImageField(upload_to='articles/covers/')
    read_time = models.DurationField(blank=True, null=True)
    published = models.BooleanField(default=True)  # Default True qilsangiz qulay
    views = models.PositiveIntegerField(default=0)
    author = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
            original_slug = self.slug
            count = 1
            while Article.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{count}"
                count += 1

        # Faqat muhim maqolani yangilash logikasi
        if self.important:
            Article.objects.filter(important=True).exclude(pk=self.pk).update(important=False)

        super().save(*args, **kwargs)

class Context(models.Model):
    # null=True va blank=True qo'shildi
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='contexts', null=True, blank=True)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='articles/contents/', blank=True, null=True)

class Comment(models.Model):
    # null=True va blank=True qo'shildi
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.email


class Moment(models.Model):
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='moments/')
    author = models.CharField(max_length=255, blank=True, null=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.title


class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"{self.name} - {self.subject}"

    def clean(self):  # Validation save'dan ko'ra clean'da to'g'riroq ishlaydi
        if not self.phone_number and not self.email:
            raise ValidationError("Telefon raqam yoki email kiriting.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)