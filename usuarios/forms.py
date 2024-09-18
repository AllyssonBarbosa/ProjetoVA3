from django import forms
from django.contrib.auth.models import Group
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    tipo_usuario = forms.ChoiceField(
        choices=[('administrador', 'Administrador'), ('limitado', 'Limitado')],
        required=True,
        widget=forms.Select
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'tipo_usuario')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
