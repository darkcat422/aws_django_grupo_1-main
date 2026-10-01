from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify





# Modelo para categorias de posts, donde cada categoria tiene un nombre unico, un slug unico generado automaticamente y una descripcion opcional
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    #slug: campo para URL amigable basado en el nombre
    slug = models.SlugField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    #slug se genera automaticamente a partir del nombre al guardar ejemplo: "Mi Categoria" -> "mi-categoria"
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
# Modelo para el perfil de usuario, extendiendo el modelo User de Django con una biografia y fecha de registro
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    biografia = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"
    
# Modelo para posts del blog, con titulo, contenido, extracto, categoria, fechas, autor, imagen y contador de vistas
class Post(models.Model):
    # Título: CharField es para texto corto (max 200 caracteres)
    titulo = models.CharField(max_length=200)

    slug = models.SlugField(max_length=200, unique=True, blank=True)    
    
    # Contenido: TextField es para texto largo sin límite predefinido
    contenido = models.TextField()

    extracto = models.CharField(max_length=300, blank=True)

    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)

    
    # Fecha: DateTimeField guarda fecha y hora. 
    # auto_now_add=True guarda automáticamente el momento exacto de creación.
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Autor: ForeignKey crea una relación con el modelo User.
    # on_delete=models.CASCADE significa que si se borra el usuario, se borran sus posts.
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Imagen: ImageField permite subir archivos. 
    # upload_to define la subcarpeta donde se guardarán.
    # null=True y blank=True permiten que la imagen sea opcional.
    imagen = models.ImageField(upload_to='blog_imagenes/', null=True, blank=True)

    vistas = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        # Esto define cómo se ve el post en el panel de admin (por su título)
        return self.titulo

# Modelo para comentarios en los posts, con relación al post, autor (usuario o nombre), texto y fecha
class Comentario(models.Model):
    # Relación con Post: related_name permite acceder a los comentarios desde un post (post.comentarios.all())
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    autor_usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    autor_nombre = models.CharField(max_length=100, blank=True) # Nombre de quien comenta
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    # Representación del comentario, mostrando el autor (usuario o nombre)
    def __str__(self):
        if self.autor_usuario:
            return f"Comentario de {self.autor_usuario.username}"
        return f"Comentario de {self.autor_nombre}"

