from django import forms
from .models import (
    Empresa,
    Matriz,
    OrdemServico,
    CategoriaParametro,
    TipoParametro,
    Parametro,
    Servico,
    Legislacao,
    VisitaTecnica,
    Amostra,
    ServicoContratado
)


class MatrizForm(forms.ModelForm):

    class Meta:
        model = Matriz
        fields = [
            "descricao",
        ]


class EmpresaForm(forms.ModelForm):

    class Meta:
        model = Empresa
        fields = [
            "apelido",
            "razao_social",
            "endereco",
            "telefone",
            "cnpj",
            "tipo_empresa",
            "email",
            "responsavel_tecnico",
        ]


class CategoriaParametroForm(forms.ModelForm):
    class Meta:
        model = CategoriaParametro
        fields = [
            "descricao",
        ]


class TipoParametroForm(forms.ModelForm):
    class Meta:
        model = TipoParametro
        fields = [
            "descricao",
        ]


class ParametroForm(forms.ModelForm):

    class Meta:
        model = Parametro
        fields = [
            "descricao",
            "unidade_medida",
            "categoria_parametro",
            "tipo_parametro",
        ]
        labels = {
            "descricao": "Descrição",
            "unidade_medida": "Unidade de Medida",
            "categoria_parametro": "Categoria",
            "tipo_parametro": "Tipo",
        }


class ServicoForm(forms.ModelForm):

    class Meta:
        model = Servico
        fields = ["descricao", "matriz"]

        widgets = {
            "descricao": forms.Textarea(
                attrs={"rows": 1, "placeholder": "Descreva o serviço"}
            ),
            "matriz": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "descricao": "Descrição do Serviço",
            "matriz": "Matriz",
        }


class OrdemServicoForm(forms.ModelForm):

    servicos = forms.ModelMultipleChoiceField(
        label="Serviços",
        help_text="Selecione um ou mais serviços",
        queryset=Servico.objects.all(),
        required=True,
    )

    class Meta:
        model = OrdemServico
        fields = [
            "empresa",
            "servicos",
            "observacoes",
        ]

        widgets = {
            "empresa": forms.Select(attrs={"class": "form-control"}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


# class OrdemServicoResultadosForm(forms.ModelForm):
#     ...


class LegislacaoForm(forms.ModelForm):

    class Meta:
        model = Legislacao
        fields = [
            "parametro",
            "valor_maximo",
            "observacao",
        ]

        widgets = {
            "parametro": forms.Select(attrs={"class": "form-control"}),
        }


class VisitaTecnicaForm(forms.ModelForm):
    class Meta:
        model = VisitaTecnica
        fields = "__all__"
        fields = [
            "ordem_servico",
            "data_visita",
            "hora_visita",
            "local",
            "responsavel",
            "observacoes",
            "status",
        ]
        widgets = {
            "data_visita": forms.DateInput(attrs={"type": "date"}),
            "hora_visita": forms.TimeInput(attrs={"type": "time"}),
            "observacoes": forms.Textarea(attrs={"rows": 3}),
            "status": forms.Select(),
        }


class CustomCharField(forms.CharField):
    def __init__(self, label, *args, **kwargs):
        super().__init__(label=label, required=False, *args, **kwargs)


def customize_ordem_servico_resultado_form(
    fields: list[dict[str, str]],
) -> forms.ModelForm:
    """
    ref. https://jacobian.org/2010/feb/28/dynamic-form-generation/
    """

class OrdemServicoResultadosForm(forms.ModelForm):

         class Meta:
             model = OrdemServico
             fields = []

         def __init__(self, *args, **kwargs):
             super().__init__(*args, **kwargs)

             for item in fields:
                 field, label, initial = (
                     item["field"],
                     item["label"],
                     item.get("initial"),
                 )
                 self.fields[field] = CustomCharField(label=label, initial=initial)
                 self.Meta.fields.append(field)
                 return OrdemServicoResultadosForm

class AmostraForm(forms.ModelForm):
    class Meta:
        model = Amostra
        fields = [
            "servico_contratado",
            "data_coleta",
            "hora_coleta",
            "local_coleta",
            "numero_ssl",
        ]
        widgets = {
            "data_coleta": forms.DateInput(attrs={"type": "date"}),
            "hora_coleta": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔹 Caso queira filtrar os serviços contratados por alguma OS (opcional)
        if "ordem_servico" in self.data:
            try:
                ordem_id = int(self.data.get("ordem_servico"))
                self.fields["servico_contratado"].queryset = ServicoContratado.objects.filter(
                    ordem_servico_id=ordem_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["servico_contratado"].queryset = ServicoContratado.objects.filter(
                ordem_servico=self.instance.servico_contratado.ordem_servico
            )
        else:
            self.fields["servico_contratado"].queryset = ServicoContratado.objects.all()

class ServicoContratadoForm(forms.ModelForm):
    class Meta:
        model = ServicoContratado
        fields = ["ordem_servico", "servico", "quantidade_amostras"]
        # widgets = {
        #     "ordem_servico": forms.Select(attrs={"class": "form-select", "onchange": "this.form.submit();"}),
        #     "servico": forms.Select(attrs={"class": "form-select"}),
        #     "quantidade_amostras": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        # }
        # labels = {
        #     "ordem_servico": "Ordem de Serviço",
        #     "servico": "Serviço",
        #     "quantidade_amostras": "Quantidade de Amostras",
        # }

