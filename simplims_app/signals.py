from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Amostra, VisitaTecnica


@receiver(post_save, sender=Amostra)
def criar_visita_tecnica_para_amostra(sender, instance, created, **kwargs):
    if not created:
        return

    # Tenta pegar Ordem de Serviço da Amostra
    servico = instance.servico_contratado
    ordem_servico = getattr(servico, "ordem_servico", None)

    # Cria a visita técnica (ordem_servico pode ser NULL)
    VisitaTecnica.objects.create(
        ordem_servico=ordem_servico,   # ← se existir, preenche
        data_visita=instance.data_coleta,
        hora_visita=instance.hora_coleta,
        local=instance.local_coleta,
        responsavel="A definir",
        status="PENDENTE",
    )
