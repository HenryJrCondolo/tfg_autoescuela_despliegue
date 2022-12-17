from rest_framework.serializers import ModelSerializer
from autoescuela.models import Examen, Examen_Usuario, Pregunta, Permiso, Tema, Usuario

class TemaSerializer(ModelSerializer):
    class Meta:
        model = Tema
        fields = ['id_Tema', 'tema', 'descripcion']

class PermisoSerializer(ModelSerializer):
    class Meta:
        model = Permiso
        fields = ['tipo_licencia', 'descripcion', 'precio']

class PreguntaSerializer(ModelSerializer):
    class Meta:
        model = Pregunta
        fields = ['id_Pregunta', 'permiso', 'tema', 'pregunta', 'respuesta_Correcta', 'respuesta_Falsa_1', 'respuesta_Falsa_2', 'imagen_pregunta', 'descripcion_adicional']

class ExamenSerializer(ModelSerializer):
    class Meta:
        model = Examen
        fields = ['id_Examen', 'nombre_Examen', 'preguntas']

class UsuarioSerializer(ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['dni', 'nombre', 'apellidos', 'email', 'telefono','groups','is_administrador', 'direccion', 'fecha_nacimiento', 'fecha_baja', 'permiso', 'imagen_usuario']

class Examen_UsuarioSerializer(ModelSerializer):
    class Meta:
        model = Examen_Usuario
        fields = ['id_Examen_Usuario', 'examen', 'usuario', 'fecha', 'preguntas_falladas', 'aprobado']

class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['dni', 'nombre', 'apellidos', 'email', 'telefono', 'groups','direccion', 'fecha_nacimiento', 'fecha_baja', 'permiso', 'imagen_usuario']

class cargarExamenesUsuarioSerializer(ModelSerializer):
    class Meta:
        model = Examen_Usuario
        fields = ['id_Examen_Usuario', 'examen', 'usuario', 'fecha', 'preguntas_falladas', 'aprobado']        