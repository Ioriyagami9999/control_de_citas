from django import forms
from citas.models import Cita
from django import forms
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import User




class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha_hora', 'tipo_cita', 'medico']  # No incluyas 'paciente' si la vas a asignar automáticamente
        widgets = {
            'fecha_hora': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'tipo_cita': forms.Select(attrs={'class': 'form-control'}),
            'medico': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))
    password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Contraseña'}))
    
    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password_confirmation(self):
        password = self.cleaned_data.get("password")
        password_confirmation = self.cleaned_data.get("password_confirmation")
        if password != password_confirmation:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password_confirmation
