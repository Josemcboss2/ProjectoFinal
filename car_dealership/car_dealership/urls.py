from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el panel de administración
    path('', include('autos.urls')),  # Redirige la ruta raíz a la aplicación 'autos'
]