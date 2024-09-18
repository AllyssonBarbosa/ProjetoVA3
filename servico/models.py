from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Servico(models.Model):
    servico_prestado = models.CharField(max_length=255)
    valor_cobrado = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(default=now)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.servico_prestado
