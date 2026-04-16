from main.models import Article

def run():
    articles = Article.objects.all()
    count = 0
    for article in articles:
        if not article.slug:
            # article.save() uses the logic to generate slug from title if missing
            article.save()
            count += 1
            print(f"Generated slug for: {article.title}")
    
    print(f"Total updated: {count}")

if __name__ == "__main__":
    run()
