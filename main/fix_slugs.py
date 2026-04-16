from main.models import Article

# Get all articles
articles = Article.objects.all()
print(f"Total articles found in database: {articles.count()}")

count = 0
for article in articles:
    # If slug is missing or just spaces, generate it
    if not article.slug or article.slug.strip() == "":
        article.save() # This triggers our custom save() with slugify
        count += 1
        print(f"Generated slug for: '{article.title}' -> '{article.slug}'")
    
    # Also ensure they are published if you want them to show up
    if not article.published:
        article.published = True
        article.save()
        print(f"Set as published: '{article.title}'")

print(f"Successfully updated {count} articles.")
