from django.urls import path
from . import views
#url de crud para la aplicacion blog (posts: listar, crear, ver detalle, editar, eliminar; perfil usuario)
urlpatterns = [
    path('', views.lista_posts, name='lista_posts'),
    path('crear/', views.crear_post, name='crear_post'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('<slug:slug>/', views.detalle_post, name='detalle_post'),
    path('<slug:slug>/editar/', views.editar_post, name='editar_post'),
    path('<slug:slug>/eliminar/', views.eliminar_post, name='eliminar_post'),
]


