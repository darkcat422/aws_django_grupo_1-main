from django.contrib import admin
from django.urls import path, include, reverse
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.http import HttpResponse

# Vista para redirigir la página de inicio al home
def inicio(request):
    return redirect(reverse('home'))

# no salage error 404 del favicon porque aun no se ha agregado uno, y el navegador lo pide automaticamente
def empty_favicon(request):
    return HttpResponse(status=204)

urlpatterns = [

    path("", inicio, name="inicio"), 
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path('accounts/', include('django.contrib.auth.urls')),#urls por defecto de django para manejo de login, logout, cambio de contraseña, etc
    path('blog/', include('blog.urls')),#urls de la aplicacion blog para posts (crear, editar, eliminar, ver detalle)
    path('pages/', include('pages.urls')),#urls de la aplicacion pages para home

    path('favicon.ico', empty_favicon),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)