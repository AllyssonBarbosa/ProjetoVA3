from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True)
    foto = models.ImageField(upload_to='core/static/fotos_produtos', blank=True, null=True)

    def __str__(self):
        return self.nome


from django.db import models
from django.utils import timezone
from core.models import Produto
from django.contrib.auth import get_user_model

class Venda(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data_venda = models.DateField(default=timezone.now)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    foto = models.ImageField(upload_to='core/static/fotos_produtos', blank=True, null=True)

    def __str__(self):
        return f'{self.produto.nome} - {self.data_venda}'
