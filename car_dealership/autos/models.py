from django.db import models

class Car(models.Model):
    CATEGORY_CHOICES = [
        ('sedan', 'Sedán'),
        ('suv', 'SUV'),
        ('sports', 'Deportivo'),
        ('pickup', 'Pickup')
    ]
    
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image_url = models.URLField(max_length=500, blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True, blank=True)
    
    def __str__(self):
        return f"{self.year} {self.brand} {self.model}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image_url = models.URLField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.name}"
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.name} en {self.article.title}"
    


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email