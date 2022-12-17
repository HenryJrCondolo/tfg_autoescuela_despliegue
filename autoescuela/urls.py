from django.urls import re_path as url
from django.views.generic import RedirectView
from .views import RegistrarUsuario,infoAutoescuela,EliminarPregunta,RegistrarExamenAuto,EditarExamen,RegistrarExamen,ListadoExamenes,EliminarExamen,EditarPregunta,ListadoPreguntas,RegistrarPregunta,EliminarUsuario,EliminarPermiso,RegistrarPermiso,ListadoPermisos,EditarPermiso,EliminarTema,EditarTema,ListadoTemas,RegistrarTema,EditarUsuario, ListadoUsuarios,index,PermisosListView,IndexExamenListView,PregruntasListView,UsuarioView
from django.urls import include, path, re_path


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^nosotros/$', infoAutoescuela, name='info_autoescuela'),
    url(r'^permisos/$', PermisosListView.as_view(), name='permisos'),
    url(r'^aula_virtual/$', IndexExamenListView.as_view(), name='aula_virtual'),
    url(r'^preguntas/(?P<pk>\d+)/$', PregruntasListView.as_view(), name='aula_virtual'),
]
urlpatterns += [url(r'^perfil_aula/$', UsuarioView.as_view(), name='perfil_aula'),]
urlpatterns += [url(r'^creacion_usuario/$', RegistrarUsuario.as_view(), name='registar_usuario'),
                url(r'^administracion_usuarios/$', ListadoUsuarios.as_view(), name='listar_usuarios'),
                path('modificacion_usuario/<slug:pk>/',  EditarUsuario.as_view(), name='modificar_usuarios'),
                path('eliminacion_usuario/<slug:pk>/',  EliminarUsuario.as_view(), name='eliminar_usuarios'),
                ]
urlpatterns += [url(r'^creacion_tema/$', RegistrarTema.as_view(), name='registar_tema'),
                url(r'^administracion_temas/$', ListadoTemas.as_view(), name='listar_temas'),
                path('modificacion_tema/<slug:pk>/',  EditarTema.as_view(), name='modificar_tema'),
                path('eliminacion_tema/<slug:pk>/',  EliminarTema.as_view(), name='eliminar_tema'),
                ]

urlpatterns += [url(r'^creacion_permiso/$', RegistrarPermiso.as_view(), name='registar_permiso'),
                url(r'^administracion_permisos/$', ListadoPermisos.as_view(), name='listar_permisos'),
                path('modificacion_permiso/<slug:pk>/',  EditarPermiso.as_view(), name='modificar_permiso'),
                path('eliminacion_permiso/<slug:pk>/',  EliminarPermiso.as_view(), name='eliminar_permiso'),
                ]
urlpatterns += [url(r'^creacion_pregunta/$', RegistrarPregunta.as_view(), name='registar_pregunta'),
                url(r'^administracion_preguntas/$', ListadoPreguntas.as_view(), name='listar_preguntas'),
                path('modificacion_pregunta/<slug:pk>/',  EditarPregunta.as_view(), name='modificar_pregunta'),
                path('eliminacion_pregunta/<slug:pk>/',  EliminarPregunta.as_view(), name='eliminar_pregunta'),
                ]
urlpatterns += [url(r'^creacion_examen/$', RegistrarExamen.as_view(), name='registar_examen'),
                url(r'^creacion_examen_automatico/$', RegistrarExamenAuto.as_view(), name='registar_examen_auto'),
                url(r'^administracion_examenes/$', ListadoExamenes.as_view(), name='listar_examenes'),
                path('modificacion_examen/<slug:pk>/',  EditarExamen.as_view(), name='modificar_examen'),
                path('eliminacion_examen/<slug:pk>/',  EliminarExamen.as_view(), name='eliminar_examen'),
                ]


