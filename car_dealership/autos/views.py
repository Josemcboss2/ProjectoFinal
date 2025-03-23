
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from .models import Car, Article, ContactMessage
from .forms import ContactForm

def home(request):
    featured_cars = Car.objects.filter(featured=True)[:5]
    latest_articles = Article.objects.order_by('-created_at')[:3]
    return render(request, 'home.html', {
        'featured_cars': featured_cars,
        'latest_articles': latest_articles
    })

def cars(request):
    category = request.GET.get('category')
    if category:
        cars_list = Car.objects.filter(category=category)
    else:
        cars_list = Car.objects.all()
    return render(request, 'cars.html', {'cars': cars_list})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'car_detail.html', {'car': car})

def articles(request):
    articles_list = Article.objects.order_by('-created_at')
    return render(request, 'articles.html', {'articles': articles_list})

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'article_detail.html', {'article': article})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # Send email
            send_mail(
                subject=f'Nuevo mensaje de {form.cleaned_data["name"]}',
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=['contact@autoelite.com'],
                fail_silently=False,
            )
            messages.success(request, 'Mensaje enviado correctamente. Nos pondremos en contacto pronto.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def privacy(request):
    return render(request, 'privacy.html')

def car_inquiry(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Obtén el coche relacionado con la consulta
        car = Car.objects.get(id=car_id)

        # Envía un correo electrónico
        send_mail(
            subject=f'Consulta sobre {car.brand} {car.model}',
            message=f'Nombre: {name}\nEmail: {email}\nTeléfono: {phone}\nMensaje: {message}',
            from_email=email,
            recipient_list=['contacto@autoelite.com'],  # Cambia esto por tu correo
            fail_silently=False,
        )

        messages.success(request, 'Tu consulta ha sido enviada. Nos pondremos en contacto contigo pronto.')
        return redirect('car_detail', car_id=car_id)
    else:
        return redirect('home')