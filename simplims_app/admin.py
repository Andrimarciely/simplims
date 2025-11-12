from django.contrib import admin

from simplims_app.models import (
    Empresa,
    Legislacao,
    Matriz,
    OrdemServico,
    CategoriaParametro,
    TipoParametro,
    Parametro,
    Servico,
    VisitaTecnica,
    Amostra,
    ServicoContratado
)

# Register your models here.
admin.site.register(Matriz)
admin.site.register(Empresa)
admin.site.register(CategoriaParametro)
admin.site.register(TipoParametro)
admin.site.register(Parametro)
admin.site.register(Servico)
admin.site.register(OrdemServico)
# admin.site.register(Amostra)
# admin.site.register(ResultadoAmostraParametro)
admin.site.register(Legislacao)
admin.site.register(VisitaTecnica)
admin.site.register(Amostra)
admin.site.register(ServicoContratado)
