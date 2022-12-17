from django.contrib import admin
from .models import Tema, Permiso, Pregunta, Usuario, Examen, Examen_Usuario

# Register your models here.
from django.contrib import admin
from .models import Tema, Permiso, Pregunta, Usuario, Examen, Examen_Usuario

# Register your models here.

@admin.register(Tema) # Register the admin class with the associated model
class TemaAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the list view
    list_display = ('tema', 'descripcion')
    fields = ['tema', 'descripcion']
    
@admin.register(Permiso) # Register the admin class with the associated model
class PermisoAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the list view
    list_display = ('tipo_licencia', 'precio')
    fields = ['tipo_licencia', 'descripcion', 'precio']


@admin.register(Pregunta) # Register the admin class with the associated model
class PreguntaAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the list view
    list_display = ('permiso', 'tema', 'pregunta', 'respuesta_Correcta','respuesta_Falsa_1', 'respuesta_Falsa_2', 'imagen_pregunta')
    fields = [('permiso', 'tema'), 'pregunta', 'respuesta_Correcta', 'respuesta_Falsa_1','respuesta_Falsa_2', 'imagen_pregunta', 'descripcion_adicional']


@admin.register(Usuario) # Register the admin class with the associated model
class UsuarioAdmin(admin.ModelAdmin):
   
    # Define the fields to be displayed in the list view
    list_display = ('dni', 'nombre', 'apellidos', 'email','password', 'is_administrador', 'telefono', 'direccion', 'fecha_nacimiento', 'fecha_baja', 'permiso', 'imagen_usuario')
    fields = ['dni','nombre', 'apellidos','password', 'email', 'telefono','is_administrador', 'is_active', 'direccion', 'fecha_nacimiento', 'fecha_baja', 'permiso', 'imagen_usuario']


@admin.register(Examen) # Register the admin class with the associated model
class ExamenAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the list view
    list_display = ('id_Examen','nombre_Examen')
    fields = ['nombre_Examen', 'preguntas']
    
@admin.register(Examen_Usuario) # Register the admin class with the associated model
class Examen_UsuarioAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the list view
    list_display = ('usuario', 'examen', 'fecha', 'display_preguntas_falladas', 'aprobado')
    fields = ['usuario', 'examen', 'fecha', 'preguntas_falladas', 'aprobado']
