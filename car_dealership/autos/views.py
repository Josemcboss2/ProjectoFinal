from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from .models import Car, Article, ContactMessage, Category
from .forms import ContactForm
from .models import Article, Comment
from .models import Subscriber
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from .forms import ContactForm
from django.http import JsonResponse
from django.template.loader import render_to_string

def home(request):
    featured_cars = Car.objects.all().order_by('-id')[:3]  # Últimos 3 coches
    latest_articles = Article.objects.order_by('-created_at')[:3]
    return render(request, 'home.html', {
        'featured_cars': featured_cars,
        'latest_articles': latest_articles
    })

def cars(request):
    # Obtener todos los carros inicialmente
    cars_list = Car.objects.all()
    
    # Filtrar por categoría
    category = request.GET.get('category')
    if category:
        cars_list = cars_list.filter(category=category)
    
    # Filtrar por marca
    brand = request.GET.get('brand')
    if brand:
        cars_list = cars_list.filter(brand=brand)
    
    # Filtrar por año
    year = request.GET.get('year')
    if year:
        cars_list = cars_list.filter(year=year)
    
    # Filtrar por precio máximo
    max_price = request.GET.get('max_price')
    if max_price:
        cars_list = cars_list.filter(price__lte=max_price)
    
    # Ordenar resultados
    sort = request.GET.get('sort')
    if sort:
        if sort == 'price_asc':
            cars_list = cars_list.order_by('price')
        elif sort == 'price_desc':
            cars_list = cars_list.order_by('-price')
        elif sort == 'year_desc':
            cars_list = cars_list.order_by('-year')
    
    # Obtener años únicos para el filtro
    years = Car.objects.values_list('year', flat=True).distinct().order_by('-year')
    
    # Obtener marcas únicas para el filtro
    brands = Car.objects.values('brand').distinct().order_by('brand')
    
    context = {
        'cars': cars_list,
        'years': years,
        'brands': brands,
        'selected_category': category,
        'selected_year': year,
        'selected_brand': brand,
        'max_price': max_price
    }
    
    return render(request, 'cars.html', context)

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    related_cars = Car.objects.exclude(id=car_id)[:3]
    return render(request, 'car_detail.html', {
        'car': car,
        'related_cars': related_cars
    })

def articles(request):
    articles_list = Article.objects.all()
    categories = Category.objects.all()
    
    # Filtrar por categoría
    category = request.GET.get('category')
    if category:
        articles_list = articles_list.filter(category__slug=category)
    
    context = {
        'articles': articles_list,
        'categories': categories,
        'selected_category': category
    }
    return render(request, 'articles.html', context)

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'article_detail.html', {'article': article})



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Procesa el formulario (envía el email, etc.)
            name = form.cleaned_data['name']
            
            # Si es una petición AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'¡Gracias {name}! Tu mensaje ha sido enviado.'
                })
            else:
                return HttpResponse('¡Mensaje enviado!')
        
        # Si hay errores
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': dict(form.errors.items())
            }, status=400)
    
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


def article_comment(request, article_id):
    if request.method == 'POST':
        article = get_object_or_404(Article, id=article_id)
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment_text = request.POST.get('comment')

        # Guarda el comentario en la base de datos
        Comment.objects.create(
            article=article,
            name=name,
            email=email,
            comment=comment_text
        )

        messages.success(request, 'Tu comentario ha sido enviado. ¡Gracias!')
        return redirect('article_detail', article_id=article_id)
    else:
        return redirect('home')

    
def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            Subscriber.objects.create(email=email)
            messages.success(request, '¡Gracias por suscribirte!')
        except:
            messages.error(request, 'Este correo ya está suscrito.')
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    return redirect('home')