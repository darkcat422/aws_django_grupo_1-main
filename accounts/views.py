from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
#creacion deo objeto para la base de datos de usuarios
class SignUpView(CreateView):
    #formulario para crear un nuevo usuario
    form_class = UserCreationForm
    #archvio paa registrar el usuario
    template_name = 'registration/signup.html'
    #redireccionar al login despues de registrarse
    success_url = reverse_lazy('login')
