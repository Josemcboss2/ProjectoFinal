from django.db import models

class Car(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=[('sedan', 'Sedán'), ('suv', 'SUV'), ('sports', 'Deportivo'), ('pickup', 'Pickup')])
    condition = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='cars/')
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.year} {self.brand} {self.model}"

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
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