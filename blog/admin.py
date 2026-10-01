from django.contrib import admin
from .models import Post, Comentario, Categoria, PerfilUsuario
#list_play: campos que se muestran en la lista del admin
#search_fields: campos por los que se puede buscar
#list_filter: filtros laterales para facilitar la busqueda
#prepopulated_fields: campos que se autocompletan basados en otros campos
#readonly_fields: campos que son solo de lectura en el admin

#funcion categoria admin para personalizar la vista de categorias en el admin, mostrando nombre y slug, y permitiendo buscar por nombre
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    search_fields = ('nombre',)
    prepopulated_fields = {'slug': ('nombre',)}

#funcion perfil usuario admin para personalizar la vista de perfiles de usuario en el admin, mostrando usuario y fecha de registro, permitiendo buscar por nombre de usuario y filtrando por fecha de registro
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_registro')
    search_fields = ('usuario__username',)
    list_filter = ('fecha_registro',)

    fieldsets = (
        ("información del usuario", {
            'fields': ('usuario',)}),
        ("Detalles del perfil", {
            'fields': ('biografia',),
            'classes': ('collapse',)}),
        ("Fecha de registro", {
            'fields': ('fecha_registro',),
            'classes': ('collapse',)}),
    )
    readonly_fields = ('fecha_registro',)


#funcion post admin para personalizar la vista de posts en el admin, mostrando titulo, autor, categoria, fecha de publicacion y vistas, permitiendo buscar por titulo y contenido, filtrando por categoria, fecha de publicacion y autor
class PostAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "categoria", "fecha_publicacion", "vistas")
    search_fields = ("titulo", "contenido")
    list_filter = ("categoria", "fecha_publicacion", "autor")
    prepopulated_fields = {"slug": ("titulo",)}

    fieldsets = (('informacion del post', {
        'fields': ('titulo', 'slug', 'extracto')}),
        ('categoria del post', {
            'fields': ('categoria',)}),
        ('contenido del post', {
            'fields': ('contenido', 'imagen')}),
        ('informacion adicional', {
            'fields': ('autor', 'fecha_publicacion', 'fecha_actualizacion', 'vistas'),
            'classes': ('collapse',)}),
    )

    readonly_fields = ('fecha_publicacion', 'fecha_actualizacion', 'vistas')
            


#funcion comentario admin para personalizar la vista de comentarios en el admin, mostrando post, autor, fecha, permitiendo buscar por autor y texto, filtrando por fecha
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("post", "autor_usuario", "autor_nombre", "fecha")
    search_fields = ("autor_nombre", "texto")
    list_filter = ("fecha",)





# Registramos los modelos para que aparezcan en el admin
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(PerfilUsuario, PerfilUsuarioAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comentario, ComentarioAdmin)

