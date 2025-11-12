from django.db import models


class VisitaTecnica(models.Model):
    STATUS_CHOICES = [
        ("PENDENTE", "Pendente"),
        ("CONFIRMADA", "Confirmada"),
        ("REALIZADA", "Realizada"),
        ("CANCELADA", "Cancelada"),
    ]

    ordem_servico = models.ForeignKey(
        "OrdemServico",
        on_delete=models.CASCADE,
    )

    data_visita = models.DateField(verbose_name="Data da Visita")
    hora_visita = models.TimeField(verbose_name="Hora da Visita", null=True, blank=True)

    local = models.CharField(
        max_length=255,
        verbose_name="Local da Visita",
        help_text="Endereço ou ponto de coleta",
    )

    responsavel = models.CharField(max_length=100)

    observacoes = models.TextField(null=True, blank=True, verbose_name="Observações")

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="PENDENTE", verbose_name="Status"
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Visita Técnica"
        verbose_name_plural = "Visitas Técnicas"
        ordering = ["-data_visita", "-hora_visita"]

    def __str__(self):
        return f"Visita {self.data_visita} - {self.local} ({self.get_status_display()})"
