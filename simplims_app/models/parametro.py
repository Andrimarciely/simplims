from django.db import models

from simplims_app.models import TipoParametro, CategoriaParametro


class Parametro(models.Model):
    descricao = models.CharField(max_length=100)

    unidade_medida = models.CharField(
        # help_text="Unidade de medida",
        max_length=10,
        verbose_name="Unidade de Medida",
    )

    tipo_parametro = models.ForeignKey(
        TipoParametro,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    categoria_parametro = models.ForeignKey(
        CategoriaParametro,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.descricao

    class Meta:
        verbose_name = "Parametro"
        unique_together = ("descricao", "unidade_medida")
