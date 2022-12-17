from django.shortcuts import render, redirect
from .models import Usuario, Permiso, Examen_Usuario, Examen, Pregunta, Tema
from django.views.generic.list import View
from django.contrib.auth.models import Group
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import JsonResponse
from .forms import FormularioUsuario, FormularioPreguntas, FormularioPermiso, FormularioExamen, FormularioTema
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def index(request):
    return render(request, 'index.html')

def infoAutoescuela(request):
    return render(request, 'autoescuela.html')


class PregruntasListView(ListView):
    model = Pregunta

    def get_queryset(self):
        return Pregunta.objects.filter(tema__id=self.kwargs['pk'])
    template_name = 'preguntas_list.html/'


class PermisosListView(PermissionRequiredMixin, ListView):
    permission_required = 'accounts/autoescuela.view_permiso'
    model = Permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permiso_list'] = Permiso.objects.all()
        return context
    template_name = 'permisos.html/'


class IndexExamenListView(PermissionRequiredMixin, ListView):
    permission_required = 'autoescuela.view_examen'
    model = Examen
    template_name = 'aula_virtual.html/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['examen_list'] = Examen.objects.all
        return context


class ExamenUsuarioListView(LoginRequiredMixin, ListView):
    model = Examen_Usuario
    template_name = 'perfil_aula.html/'
    permission_required = 'autoescuela.view_examen_usuario'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['examen_usuario_list'] = Examen_Usuario.objects.filter(
            usuario=self.request.user.dni)
        return context


class UsuarioView(LoginRequiredMixin, View):
    PermissionRequiredMixin = 'autoescuela.view_examen'

    def get(self, request, *args, **kwargs):
        usuario = Usuario.objects.get(dni=self.request.user.dni)
        return render(request, 'perfil_aula.html', {'usuario': usuario})


class RegistrarUsuario(PermissionRequiredMixin, CreateView):
    permission_required = 'autoescuela.add_usuario'
    model = Usuario
    form_class = FormularioUsuario

    template_name = 'gestion_usuarios/create_user.html'
    success_url = 'listar_usuarios'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            nuevo_usuario = Usuario(
                dni=form.cleaned_data['dni'],
                nombre=form.cleaned_data['nombre'],
                apellidos=form.cleaned_data['apellidos'],
                imagen_usuario=form.cleaned_data['imagen_usuario'],
                email=form.cleaned_data['email'],
                telefono=form.cleaned_data['telefono'],
                direccion=form.cleaned_data['direccion'],
                fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                permiso=form.cleaned_data['permiso'],
                
                is_active=True,
                is_administrador=form.cleaned_data['is_administrador'],
            )
            
            
            nuevo_usuario.set_password(form.cleaned_data['password1'])
            nuevo_usuario.save()
            for g in form.cleaned_data['groups']:
                Group.objects.get(name=g)
                nuevo_usuario.groups.add(g)
            return redirect('listar_usuarios')
        else:
            return render(request, self.template_name, {'form': form})


class ListadoUsuarios(PermissionRequiredMixin, ListView):
    permission_required = 'autoescuela.view_usuario'
    model = Usuario
    template_name = 'gestion_usuarios/administracion_user.html'
    paginate_by = 5

    def get_queryset(self):
        if(self.request.GET.get('buscar')):
            queryset = self.request.GET.get('buscar')
            usuarios = Usuario.objects.filter(Q(dni__icontains=queryset) | Q(nombre__icontains=queryset) | Q(apellidos__icontains=queryset) | Q(email__icontains=queryset) | Q(telefono__icontains=queryset))
            usuarios = usuarios.filter(is_active=True)
            
        else:
            usuarios = Usuario.objects.filter(is_active=True)
              
        paginator = Paginator(usuarios, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            usuarios = paginator.page(page)
        except PageNotAnInteger:
            usuarios = paginator.page(1)
        except EmptyPage:
            usuarios = paginator.page(paginator.num_pages)
        return usuarios


class EditarUsuario(PermissionRequiredMixin, UpdateView):
    permission_required = 'autoescuela.change_usuario'
    model = Usuario
    template_name = 'gestion_usuarios/modify_user.html/'
    form_class = FormularioUsuario
    def change_groups(self, form):
        for g in form.cleaned_data['groups']:
            Group.objects.get(name=g)
            self.object.groups.add(g)
    success_url = reverse_lazy('listar_usuarios')


class EliminarUsuario(PermissionRequiredMixin, DeleteView):
    permission_required = 'autoescuela.delete_usuario'
    model = Usuario
    success_url = reverse_lazy('listar_usuarios')


class RegistrarPregunta(PermissionRequiredMixin, CreateView):
    permission_required = 'autoescuela.add_pregunta'
    model = Pregunta
    form_class = FormularioPreguntas
    template_name = 'gestion_preguntas/create_preguntas.html'
    success_url = reverse_lazy('listar_preguntas')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            nueva_pregunta = Pregunta(
                pregunta=form.cleaned_data['pregunta'],
                imagen_pregunta=form.cleaned_data['imagen_pregunta'],
                respuesta_correcta=form.cleaned_data['respuesta_correcta'],
                respuesta_incorrecta_1=form.cleaned_data['respuesta_incorrecta_1'],
                respuesta_incorrecta_2=form.cleaned_data['respuesta_incorrecta_2'],
                respuesta_incorrecta_3=form.cleaned_data['respuesta_incorrecta_3'],
                tema=form.cleaned_data['tema'],
            )
            nueva_pregunta.save()
            return redirect('listar_preguntas')
        else:
            return render(request, self.template_name, {'form': form})


class ListadoPreguntas(PermissionRequiredMixin, ListView):
    permission_required = 'autoescuela.view_pregunta'
    model = Pregunta
    template_name = 'gestion_preguntas/administracion_preguntas.html'
    
   

    def get_queryset(self):
        if(self.request.GET.get('buscar')):
            queryset = self.request.GET.get('buscar')
            tema = Tema.objects.filter(Q(tema__icontains=queryset))
            preguntas = Pregunta.objects.filter(Q(pregunta__icontains=queryset) | Q(tema__in=tema))    
        else:
            preguntas= Pregunta.objects.all()
            
        paginator = Paginator(preguntas, 5)
        page = self.request.GET.get('page')
        try:
            preguntas = paginator.page(page)
        except PageNotAnInteger:
            preguntas = paginator.page(1)
        except EmptyPage:
            preguntas = paginator.page(paginator.num_pages)
        
        return preguntas

class EditarPregunta(PermissionRequiredMixin, UpdateView):
    permission_required = 'autoescuela.change_pregunta'
    model = Pregunta
    template_name = 'gestion_preguntas/modify_preguntas.html/'
    form_class = FormularioPreguntas
    success_url = reverse_lazy('listar_preguntas')

class EliminarPregunta(PermissionRequiredMixin, DeleteView):
    permission_required = 'autoescuela.delete_pregunta'
    model = Pregunta
    success_url = reverse_lazy('listar_preguntas')

class RegistrarExamen(PermissionRequiredMixin, CreateView):
    permission_required = 'autoescuela.add_examen'
    model = Examen
    form_class = FormularioExamen
    template_name = 'gestion_examenes/create_examen.html'
    success_url = reverse_lazy('listar_examenes')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            nuevo_examen = Examen(
                nombre_Examen= form.cleaned_data['nombre_Examen'],
                preguntas = form.cleaned_data['preguntas'],
            )
            nuevo_examen.save()
            return redirect('listar_examenes')
        else:
            return render(request, self.template_name, {'form': form})

class ListadoExamenes(PermissionRequiredMixin, ListView):
    permission_required = 'autoescuela.view_examen'
    model = Examen
    template_name = 'gestion_examenes/administracion_examen.html'
    

    def get_queryset(self):
        if(self.request.GET.get('buscar')):
            queryset = self.request.GET.get('buscar')
            examen = Examen.objects.filter(Q(nombre_Examen__icontains=queryset))
        else:
            examen = Examen.objects.all()
        
        paginator = Paginator(examen, 5)
        page = self.request.GET.get('page')
        try:
            examen = paginator.page(page)
        except PageNotAnInteger:
            examen = paginator.page(1)
        except EmptyPage:
            examen = paginator.page(paginator.num_pages)
        return examen

class EditarExamen(PermissionRequiredMixin, UpdateView):
    permission_required = 'autoescuela.change_examen'
    model = Examen
    template_name = 'gestion_examenes/modify_examen.html/'
    form_class = FormularioExamen
    success_url = reverse_lazy('listar_examenes')

class EliminarExamen(PermissionRequiredMixin, DeleteView):
    permission_required = 'autoescuela.delete_examen'
    model = Examen
    success_url = reverse_lazy('listar_examenes')

class RegistrarTema(PermissionRequiredMixin, CreateView):
    permission_required = 'autoescuela.add_tema'
    model = Tema
    form_class = FormularioTema
    template_name = 'gestion_temas/create_tema.html'
    success_url = reverse_lazy('listar_temas')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            nuevo_tema = Tema(
                tema= form.cleaned_data['tema'],
                descripcion= form.cleaned_data['descripcion'],
            )
            nuevo_tema.save()
            return redirect('listar_temas')
        else:
            return render(request, self.template_name, {'form': form})

class ListadoTemas(PermissionRequiredMixin, ListView):
    permission_required = 'autoescuela.view_tema'
    model = Tema
    template_name = 'gestion_temas/administracion_temas.html'
    

    def get_queryset(self):
        if(self.request.GET.get('buscar')):
            queryset = self.request.GET.get('buscar')
            temas = Tema.objects.filter(Q(tema__icontains=queryset))
        else:
            temas = Tema.objects.all()
        
        paginator = Paginator(temas, 5)
        page = self.request.GET.get('page')
        try:
            temas = paginator.page(page)
        except PageNotAnInteger:
            temas = paginator.page(1)
        except EmptyPage:
            temas = paginator.page(paginator.num_pages)
        return temas

class EditarTema(PermissionRequiredMixin, UpdateView):
    permission_required = 'autoescuela.change_tema'
    model = Tema
    template_name = 'gestion_temas/modify_tema.html/'
    form_class = FormularioTema
    success_url = reverse_lazy('listar_temas')

class EliminarTema(PermissionRequiredMixin, DeleteView):
    permission_required = 'autoescuela.delete_tema'
    model = Tema
    success_url = reverse_lazy('listar_temas')

class RegistrarPermiso(PermissionRequiredMixin, CreateView):
    permission_required = 'autoescuela.add_permiso'
    model = Permiso
    form_class = FormularioPermiso
    template_name = 'gestion_permisos/create_permisos.html'
    success_url = reverse_lazy('listar_permisos')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            nuevo_permiso = Permiso(
                tipo_licencia= form.cleaned_data['tipo_licencia'],
                descripcion= form.cleaned_data['descripcion'],
                precio= form.cleaned_data['precio'],
            )
            nuevo_permiso.save()
            return redirect('listar_permisos')
        else:
            return render(request, self.template_name, {'form': form})

class ListadoPermisos(PermissionRequiredMixin, ListView):
    permission_required = 'autoescuela.view_permiso'
    model = Permiso
    template_name = 'gestion_permisos/administracion_permisos.html'
    

    def get_queryset(self):
        if(self.request.GET.get('buscar')):
            queryset = self.request.GET.get('buscar')
            permisos = Permiso.objects.filter(Q(tipo_licencia__icontains=queryset))
        else:
            permisos = Permiso.objects.all()
        
        paginator = Paginator(permisos, 5)
        page = self.request.GET.get('page')
        try:
            permisos = paginator.page(page)
        except PageNotAnInteger:
            permisos = paginator.page(1)
        except EmptyPage:
            permisos = paginator.page(paginator.num_pages)
        return permisos

class EditarPermiso(PermissionRequiredMixin, UpdateView):
    permission_required = 'autoescuela.change_permiso'
    model = Permiso
    template_name = 'gestion_permisos/modify_permisos.html/'
    form_class = FormularioPermiso
    success_url = reverse_lazy('listar_permisos')

class EliminarPermiso(PermissionRequiredMixin, DeleteView):
    permission_required = 'autoescuela.delete_permiso'
    model = Permiso
    success_url = reverse_lazy('listar_permisos')

class RegistrarExamenAuto(PermissionRequiredMixin, CreateView):
    permission_required = 'autoescuela.add_examen'
    model = Examen
    form_class = FormularioExamen
    template_name = 'gestion_examenes/create_examen_automatic.html'
    success_url = reverse_lazy('listar_examenes')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            nuevo_examen = Examen(
                nombre_Examen= form.cleaned_data['nombre_Examen'],
                preguntas = form.cleaned_data['preguntas'],
            )
            nuevo_examen.save()
            return redirect('listar_examenes')
        else:
            return render(request, self.template_name, {'form': form})