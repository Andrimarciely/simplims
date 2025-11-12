from django.db import models


class TipoParametro(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.descricao
