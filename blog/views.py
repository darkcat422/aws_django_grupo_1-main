from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, PerfilUsuario
from .forms import PostForm, ComentarioForm

# Vista para listar todos los posts
def lista_posts(request):
    # Obtener todos los posts ordenados por fecha (más recientes primero)
    posts = Post.objects.all().order_by('-fecha_publicacion')
    return render(request, 'blog/lista_posts.html', {'posts': posts})

# Vista para ver el detalle de un post, incluyendo comentarios y formulario para agregar comentarios
def detalle_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Contar las vistas del post
    post.vistas += 1
    post.save()

    # Obtener los comentarios asociados a este post ordenados del más reciente al más antiguo
    comentarios = post.comentarios.all().order_by('-fecha')

    # Manejar el formulario de comentarios
    if request.method == "POST":
        if request.user.is_authenticated:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                nuevo = form.save(commit=False)
                nuevo.post = post
                nuevo.autor_usuario = request.user
                nuevo.save()
                return redirect('detalle_post', slug=post.slug)
        else:
            return redirect('login')
    else:
        form = ComentarioForm()

    return render(request, "blog/detalle_post.html", {
        "post": post,
        "comentarios": comentarios,
        "form": form,
    })

# login requerido para crear, editar, eliminar posts y ver perfil de usuario, dependiendo del usuario autenticado
@login_required
def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
    
        if form.is_valid():
            nuevo = form.save(commit=False)
            nuevo.autor = request.user
            nuevo.save()
            return redirect('detalle_post', slug=nuevo.slug)
    else:
        form = PostForm()

    # Renderizar el formulario de creación de post
    return render(request, 'blog/crear_post.html', {'form': form})

# edicion de post, solo el autor puede editar su post
@login_required
def editar_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    # verificacion de autor del post
    if post.autor != request.user:
        return redirect('detalle_post', slug=post.slug)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('detalle_post', slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/crear_post.html', {'form': form, 'editar': True})

# eliminacion de post, solo el autor puede eliminar su post
@login_required
def eliminar_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # verificacion de autor del post
    if post.autor != request.user:
        return redirect('detalle_post', slug=post.slug)

    # eliminar post
    post.delete()
    return redirect('lista_posts')

# Vista para ver y editar el perfil de usuario
@login_required
def perfil_usuario(request):
    # Obtener o crear el perfil de usuario asociado al usuario autenticado
    perfil, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
    # devuelve el perfil del usuario autenticado
    return render(request, "blog/perfil.html", {"perfil": perfil})