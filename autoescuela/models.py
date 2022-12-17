from django.utils import timezone
import random
from django.db import models
from django.contrib.auth.models import Group
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
   

# Create your models here.
class Tema(models.Model):
    #Esta clase representa los temas de la autoescuela
    id_Tema =  models.AutoField(primary_key=True) #Identificador del tema
    tema = models.CharField(max_length=100) #Nombre del tema
    descripcion = models.TextField() #Descripción del tema
    
    class Meta:
        ordering = ["tema"]
    
    def __str__(self):
        return "Tema: "+self.tema
    
class Permiso(models.Model):
    #Esta clase representa a los permisos que se pueden obtener en la autoescuela
    tipo_licencia = models.CharField(primary_key=True, max_length=11, unique=True) #Tipo de licencia A, B, C, D 
    descripcion = models.TextField() #Descripción del permiso
    precio = models.FloatField(null=True, blank=True, default=0.0) #Precio del permiso
    
    class Meta:
        ordering = ["tipo_licencia"]
    def __str__(self):
        return "Permiso: "+self.tipo_licencia
     
class Pregunta(models.Model):
    #Esta clase representa a las preguntas de que generan los exámenes
    id_Pregunta = models.AutoField(primary_key=True);
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE) #Relación con la clase Tema (Muchos a uno)
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE) #Relación con la clase Permiso (Muchos a uno)
    pregunta = models.TextField()
    respuesta_Falsa_1 = models.TextField()
    respuesta_Falsa_2 = models.TextField(null=True, blank=True)
    respuesta_Correcta = models.TextField()
    imagen_pregunta = models.ImageField(upload_to='imagenes_preguntas', null=True, blank=True) #Campo para subir imágenes de las preguntas
    descripcion_adicional = models.TextField(null=True, blank=True) #Campo para añadir descripciones adicionales a la respuesta correcta
    
    class Meta:
        ordering = ["tema"]
    def __str__(self):
        return "Pregunta: "+self.pregunta+"; Tema: "+ self.tema.tema+ "; Permiso: "+self.permiso.tipo_licencia
    def ordenar_respuestas(self):
        lista_respuestas = [self.respuesta_Correcta, self.respuesta_Falsa_1, self.respuesta_Falsa_2]
        random.shuffle(lista_respuestas)
        return lista_respuestas
    
    
   
class UsuarioManager(BaseUserManager):
    def create_user(self, dni, nombre, apellidos, fecha_nacimiento, telefono, email, password=None):
        if not dni:
            raise ValueError('Los usuarios deben tener un DNI')
        user = self.model(
            dni=dni,
            nombre=nombre,
            apellidos=apellidos,
            fecha_nacimiento=fecha_nacimiento,
            telefono=telefono,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, dni, nombre, apellidos, fecha_nacimiento, telefono, email, password):
        user = self.create_user(
            dni=dni,
            nombre=nombre,
            apellidos=apellidos,
            fecha_nacimiento=fecha_nacimiento,
            email=self.normalize_email(email),
            telefono=telefono,
            password=password,
        )
        user.is_administrador = True
        user.save()
        return user
    
class Usuario(AbstractBaseUser, PermissionsMixin):
    #Esta clase representa a los usuarios de la autoescuela
    dni = models.CharField(primary_key=True, max_length=11, unique=True) #DNI del usuario
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE, null=True) #Relación con la clase Permiso (Muchos a uno)
    nombre = models.CharField(max_length=100)  #Nombre del usuario
    apellidos = models.CharField(max_length=100) 
    fecha_nacimiento = models.DateField()
    imagen_usuario = models.ImageField(upload_to='imagenes_usuarios', null=True, blank=True) #Campo para subir imágenes de los usuarios
    direccion = models.CharField(max_length=100) #Dirección del usuario
    telefono = models.CharField(max_length=9) #Teléfono del usuario
    email= models.EmailField(unique=True)  #Email del usuario
    fecha_matriculacion = models.DateTimeField(default=timezone.now) #Fecha de matriculación del usuario
    fecha_baja = models.DateField(default=None, null=True, blank=True) #Fecha de salida del usuario, es decir cuando el usuari apruebe el examen
    
    is_administrador = models.BooleanField(default=False) #Campo para saber si el usuario es administrador
    is_active = models.BooleanField(default=True) #Campo para saber si el usuario está activo
    USERNAME_FIELD = 'dni' #Campo que se utiliza para el login
    REQUIRED_FIELDS = ['nombre', 'apellidos', 'fecha_nacimiento', 'telefono', 'email'] #Campos que se deben rellenar para crear un usuario
    objects = UsuarioManager() #Objeto para el login
    groups = models.ManyToManyField(Group, blank=True) #Relación con la clase Group (Muchos a muchos)
    
    class Meta:
        ordering = ["nombre"]
    def __str__(self):
        return "DNI: "+self.dni + ", Nombre " + self.nombre + " " + self.apellidos
    
    def get_absolute_url(self):
        return reverse('usuario-detail', args=[str(self.dni)])
    
    def has_perm(self, perm, obj = None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_administrador
    
class Examen (models.Model):
    #Esta clase representa a los exámenes que se realizan en la autoescuela
    id_Examen = models.AutoField(primary_key=True) 
    nombre_Examen = models.CharField(max_length=100) #Nombre del examen
    preguntas = models.ManyToManyField(Pregunta) #Relación con la clase Pregunta (Muchos a muchos)
    
    class Meta:
        ordering = ["nombre_Examen"]
    def __str__(self):
        return "Examen: "+self.nombre_Examen
    def get_absolute_url(self):
        return reverse(self.nombre_Examen, args=[str(self.id_Examen)])
    def display_preguntas(self):
        return ', '.join(pregunta.id_Pregunta for pregunta in self.preguntas.all())
    
    @property
    def all_preguntas(self):
        return self.preguntas.all()
    
    
    
class Examen_Usuario (models.Model):
    #Esta clase representa a los exámenes realizados por los usuarios en la autoescuela
    id_Examen_Usuario = models.AutoField(primary_key=True)
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE) #Relación con la clase Examen (Muchos a uno)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE) #Relación con la clase Usuario (Muchos a uno)
    preguntas_falladas = models.ManyToManyField(Pregunta) #Relación con la clase Pregunta (Muchos a muchos)
    aprobado = models.BooleanField(default=False) #Booleano que indica si el usuario ha aprobado el examen o no
    fecha = models.DateTimeField(default=timezone.now) #Fecha en la que se realiza el examen
     
    class Meta:
        ordering = ["usuario"]
    def display_preguntas_falladas(self):
        return ', '.join(pregunta.pregunta for pregunta in self.preguntas_falladas.all())   
    def __str__(self):
        return "Examen: "+str(self.examen.id_Examen)+"; Usuario: "+str(self.usuario.nombre)+"; Preguntas falladas: "+", ".join(str(seg.id_Pregunta) for seg in self.preguntas_falladas.all())+"; Aprobado: "+str(self.aprobado)+"; Fecha: "+str(self.fecha)
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})



