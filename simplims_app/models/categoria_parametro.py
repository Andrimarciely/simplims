from django.db import models


class CategoriaParametro(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.descricao
