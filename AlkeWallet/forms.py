from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Contact


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    first_name = forms.CharField(max_length=50, label="Nombre")
    last_name = forms.CharField(max_length=50, label="Apellido")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})
        self.fields['username'].label = "Nombre de usuario"
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar contraseña"


class DepositoForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10, decimal_places=2, min_value=1,
        label="Monto a depositar",
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '0.00', 'step': '0.01'})
    )
    description = forms.CharField(
        max_length=200, required=False, label="Descripción (opcional)",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej: Recarga de saldo'})
    )


class EnvioDineroForm(forms.Form):
    destinatario = forms.ChoiceField(
        label="Destinatario",
        choices=[],
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    amount = forms.DecimalField(
        max_digits=10, decimal_places=2, min_value=0.01,
        label="Monto",
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '0.00', 'step': '0.01'})
    )
    description = forms.CharField(
        max_length=200, required=False, label="Descripción",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Motivo del envío...'})
    )


class AgregarContactoForm(forms.Form):
    nombre = forms.CharField(
        max_length=100, label="Nombre completo",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Juan García'})
    )
    email = forms.EmailField(
        required=False, label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'juan@email.com'})
    )
    numero_cuenta = forms.CharField(
        max_length=30, label="Número de cuenta",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej: 00012345678'})
    )
    tipo_cuenta = forms.ChoiceField(
        choices=Contact.TIPO_CUENTA_CHOICES, label="Tipo de cuenta",
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    banco = forms.ChoiceField(
        choices=Contact.BANCO_CHOICES, label="Banco",
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    alias = forms.CharField(
        max_length=100, required=False, label="Alias (opcional)",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej: Mi amigo Juan'})
    )
