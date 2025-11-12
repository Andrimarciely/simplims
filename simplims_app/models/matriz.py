from django.db import models


class Matriz(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.descricao

    class Meta:
        verbose_name = "Matriz"
        verbose_name_plural = "Matrizes"
