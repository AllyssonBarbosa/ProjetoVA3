# forms.py
from django import forms
from .models import Servico
from django.utils.timezone import now

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['servico_prestado', 'valor_cobrado', 'data']
        widgets = {
            'data': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):

        if not kwargs.get('instance'):
            kwargs.setdefault('initial', {})['data'] = now()
        super().__init__(*args, **kwargs)
