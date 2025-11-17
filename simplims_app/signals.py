from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Amostra, VisitaTecnica, Parametro, ParametroAmostra


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

@receiver(post_save, sender=Amostra)
def criar_parametros_para_amostra(sender, instance, created, **kwargs):
    if not created:
        return

    categorias = instance.categorias.all()

    parametros = Parametro.objects.filter(
        categoria_parametro__in=categorias
    ).distinct()

    for p in parametros:
        ParametroAmostra.objects.get_or_create(
            amostra=instance,
            parametro=p
        )