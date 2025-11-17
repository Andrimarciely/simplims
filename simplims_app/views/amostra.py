from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from ..forms import AmostraForm
from ..models import Amostra
from .mixins import DeleteRecordMixin


class AmostraViewMixin:
    """
    Mixin para views de Amostra: define model, form e URL de sucesso.
    """
    model = Amostra
    form_class = AmostraForm
    ordering = ['-id']
    success_url = reverse_lazy("amostra_listar")


class AmostraListView(AmostraViewMixin, ListView):
    # context_object_name = "amostra"
    template_name = "simplims_app/amostra/lista.html"


class AmostraCreateView(AmostraViewMixin, CreateView):
    template_name = "simplims_app/amostra/formulario.html"

    def get_initial(self):
        initial = super().get_initial()
        servico_id = self.request.GET.get("servico_contratado")
        if servico_id:
            initial["servico_contratado"] = servico_id
        return initial

    def form_valid(self, form):
        servico_id = self.request.GET.get("servico_contratado")

        if servico_id:
            form.instance.servico_contratado_id = servico_id
        else:
            form.add_error(None, "Serviço contratado não informado.")
            return self.form_invalid(form)

        # Salva a amostra normalmente
        response = super().form_valid(form)

        # Agora que self.object existe, e o ManyToMany já foi salvo,
        # gerar os ParametroAmostra corretamente.
        categorias = self.object.categorias.all()

        from simplims_app.models import Parametro, ParametroAmostra

        parametros = Parametro.objects.filter(
            categoria_parametro__in=categorias
        ).distinct()

        for p in parametros:
            ParametroAmostra.objects.get_or_create(
                amostra=self.object,
                parametro=p
            )
        # ---- AQUI TERMINA A PARTE NOVA ----

        return response

    def get_success_url(self):
        servico_id = self.object.servico_contratado_id
        return reverse_lazy("amostra_criar") + f"?servico_contratado={servico_id}"




class AmostraUpdateView(AmostraViewMixin, UpdateView):
    template_name = "simplims_app/amostra/formulario.html"



class AmostraDeleteView(AmostraViewMixin, DeleteRecordMixin, DeleteView):
    template_name = "simplims_app/amostra/confirmar_exclusao.html"

