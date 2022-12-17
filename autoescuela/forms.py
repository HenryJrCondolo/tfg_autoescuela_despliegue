from django import forms
from .models import Usuario, Examen, Pregunta, Tema, Permiso
from django.contrib.auth.forms import AuthenticationForm


class FormularioUsuario(forms.ModelForm):
    """Formulario para el modelo Usuario"""

    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la contraseña',
            'id': 'password1',
            'required': 'required',
        }
    ))
    password2 = forms.CharField(label='Repite la contraseña', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Repite la contraseña',
            'id': 'password2',
            'required': 'required',
        }
    ))

    class Meta:
        model = Usuario
        fields = ['dni', 'nombre', 'apellidos', 'email', 'imagen_usuario',
                  'telefono', 'direccion', 'fecha_nacimiento', 'permiso', 'is_administrador', 'groups']
        widgets = {
            'dni': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el DNI',
                    'id': 'dni',
                    'required': 'required',
                }
            ),
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre',
                    'id': 'nombre',
                    'required': 'required',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese los apellidos',
                    'id': 'apellidos',
                    'required': 'required',
                }
            ),
            'imagen_usuario': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la imagen',
                    'id': 'imagen_usuario',
                    'required': 'required',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el email',
                    'id': 'email',
                    'required': 'required',
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el teléfono',
                    'id': 'telefono',
                    'required': 'required',
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la dirección',
                    'id': 'direccion',
                    'required': 'required',
                }
            ),
            'fecha_nacimiento': forms.DateInput(
                attrs={
                    'class': 'form-datepicker',
                    'placeholder': 'Ingrese la fecha de nacimiento',
                    'id': 'fecha_nacimiento',
                    'type': 'date',
                    'required': 'required',
                }
            ),
            'permiso': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'permiso',
                    'required': 'required',
                }
            ),
            'is_administrador': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'id': 'is_administrador',
                    'type': 'checkbox',
                    'choices': 'is_administrador',
                }
            ),
            'groups': forms.SelectMultiple(
                attrs={
                    'class': 'form-control',
                    'id': 'groups',
                    'required': 'required',
                    'multiple': 'multiple',
                }
            )    
        }

    def clean_password2(self):
        # Comprueba que las dos contraseñas coinciden
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        # Guarda la contraseña en formato hash
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class FormularioPreguntas(forms.ModelForm):
    """Formulario para el modelo Preguntas"""

    class Meta:
        model = Pregunta
        fields = ['tema', 'permiso', 'pregunta', 'respuesta_Falsa_1', 'respuesta_Falsa_2', 'respuesta_Correcta','descripcion_adicional','imagen_pregunta']
        
        widgets = {
            
            'tema': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Seleccione el tema de la pregunta',
                    'id': 'tema',
                    'required': 'required',
                }
            ),
            'permiso': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'permiso',
                    'placeholder': 'Seleccione a que permiso pertenece la pregunta',
                    'required': 'required',
                }
            ),
            'pregunta': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la pregunta',
                    'id': 'pregunta',
                    'required': 'required',
                }
            ),
            'respuesta_Falsa_1': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la respuesta falsa 1',
                    'id': 'respuesta_Falsa_1',
                    'required': 'required',
                }
            ),
            'respuesta_Falsa_2': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la respuesta falsa 2',
                    'id': 'respuesta_Falsa_2',
                    'required': 'required',
                }
            ),
            'respuesta_Correcta': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la respuesta correcta',
                    'id': 'respuesta_Correcta',
                    'required': 'required',
                }
            ),
            'imagen_pregunta': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la imagen',
                    'id': 'imagen_pregunta',
                    'required': 'required',
                }
            ),
            'descripcion_adicional': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la descripción adicional',
                    'id': 'descripcion_adicional',
                    'required': 'required',
                }
            ),            
        }
        
class FormularioTema(forms.ModelForm):
    """Formulario para el modelo Temas"""

    class Meta:
        model = Tema
        fields = ['id_Tema','tema', 'descripcion']
        
        widgets = {
            'id_Tema': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el id del tema',
                    'id': 'id_Tema',
                    'required': 'required',
                }
            ),
            'tema': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el tema',
                    'id': 'tema',
                    'required': 'required',
                }
            ),
            'descripcion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la descripción',
                    'id': 'descripcion',
                    'required': 'required',
                }
            ),
        }
        
class FormularioExamen(forms.ModelForm):
    """Formulario para el modelo Examen"""

    class Meta:
        model = Examen
        fields = ['id_Examen','nombre_Examen', 'preguntas']
        
        widgets = {
            'id_Examen': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el id del examen',
                    'id': 'id_Examen',
                    'required': 'required',
                }
            ),
            'nombre_Examen': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre del examen',
                    'id': 'nombre_examen',
                    'required': 'required',
                }
            ),
            'preguntas': forms.SelectMultiple(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Seleccione las preguntas',
                    'id': 'preguntas',
                    'required': 'required',
                }
            ),
        }
        
class FormularioPermiso(forms.ModelForm):
    """Formulario para el modelo Permiso"""

    class Meta:
        model = Permiso
        fields = ['tipo_licencia', 'descripcion','precio']
        
        widgets = {
            'tipo_licencia': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el tipo de licencia',
                    'id': 'tipo_licencia',
                    'required': 'required',
                }
            ),
            'descripcion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la descripción',
                    'id': 'descripcion',
                    'required': 'required',
                }
            ),
            'precio': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el precio',
                    'id': 'precio',
                    'required': 'required',
                }
            ),
        }