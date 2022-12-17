from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import filters
from autoescuela.models import Examen, Examen_Usuario, Pregunta, Permiso, Tema, Usuario
from autoescuela.api.serializers import cargarExamenesUsuarioSerializer,ExamenSerializer, Examen_UsuarioSerializer, PreguntaSerializer, PermisoSerializer, TemaSerializer, UsuarioSerializer, UserLoginSerializer
from django.http import JsonResponse



class ExamenViewSet(viewsets.ModelViewSet):
    serializer_class = ExamenSerializer
    queryset = Examen.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('nombre_Examen', 'id_Examen')
    
    def get_Object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.data['id_Examen'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        logedin_user = request.user
        if logedin_user.is_superuser:
            return self.delete(request, *args, **kwargs)
        else:
            response_message = {'message': 'No se ha eliminado'}
            return Response(response_message)
        
    
class PreguntaViewSet(viewsets.ModelViewSet):
    serializer_class = PreguntaSerializer
    queryset = Pregunta.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('pregunta', 'id_Pregunta', 'tema', 'permiso')
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        logedin_user = request.user
        if logedin_user.is_superuser:
            return self.delete(request, *args, **kwargs)
        else:
            response_message = {'message': 'No se ha eliminado'}
            return Response(response_message)
    
class PermisoViewSet(viewsets.ModelViewSet):
    serializer_class = PermisoSerializer
    queryset = Permiso.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('tipo_licencia')
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        logedin_user = request.user
        if logedin_user.is_superuser:
            return self.delete(request, *args, **kwargs)
        else:
            response_message = {'message': 'No se ha eliminado'}
            return Response(response_message)
    
class TemaViewSet(viewsets.ModelViewSet):
    serializer_class = TemaSerializer
    queryset = Tema.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('nombre_Tema', 'id_Tema')
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        logedin_user = request.user
        if logedin_user.is_superuser:
            return self.delete(request, *args, **kwargs)
        else:
            response_message = {'message': 'No se ha eliminado'}
            return Response(response_message)
    
class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('nombre', 'apellidos', 'dni', 'email', 'telefono', 'dni')
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        logedin_user = request.user
        if logedin_user.is_superuser:
            return self.delete(request, *args, **kwargs)
        else:
            response_message = {'message': 'No tiene permisos para borrar usuario'}
            return Response(response_message)
        
    
class Examen_UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = Examen_UsuarioSerializer
    queryset = Examen_Usuario.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id_Examen_Usuario', 'id_Examen', 'id_Usuario')
   
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        logedin_user = request.user
        if logedin_user.is_superuser:
            return self.delete(request, *args, **kwargs)
        else:
            response_message = {'message': 'No se ha eliminado'}
            return Response(response_message)
        
    def get_usuario_class(self, *args, **kwargs):
        queryset = Examen_Usuario.objects.filter(usuario = self.request.user.dni)
        return JsonResponse({'data': list(queryset.values())})
        
class UserLoginViewSet(viewsets.ModelViewSet):
    serializer_class = UserLoginSerializer
    
    def get_queryset(self, *args, **kwargs):
        queryset = Usuario.objects.filter(dni = self.request.user.dni)
        return queryset
    
class cargarExamenesUsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = cargarExamenesUsuarioSerializer
    
    def get_queryset(self, *args, **kwargs):
        queryset = Examen_Usuario.objects.filter(usuario = self.request.user.dni)
        return queryset

