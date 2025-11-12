from django.db import models


class Empresa(models.Model):
    TIPOS = [
        ("CONSULTORIA", "Consultoria Ambiental"),
        ("CLIENTE", "Cliente"),
        ("FORNECEDOR", "Fornecedor"),
    ]

    apelido = models.CharField(
        #  help_text="Apelido ou abreviação", max_length=200, verbose_name="Apelido"
    )

    razao_social = models.CharField(
        # help_text="Razão social da empresa",
        max_length=200,
        verbose_name="Razão Social",
    )

    endereco = models.CharField(
        # help_text="Endereço completo",
        max_length=200,
        verbose_name="Endereço",
    )

    telefone = models.CharField(
        # help_text="Telefone para contato",
        max_length=15,
        verbose_name="Telefone/Fax",
    )

    cnpj = models.CharField(
        # help_text="CNPJ",
        max_length=20,
        verbose_name="CNPJ",
    )

    tipo_empresa = models.CharField(
        max_length=20,
        choices=TIPOS,
        verbose_name="Tipo de Empresa",
    )

    email = models.EmailField(
        blank=True,
        null=True,
        # help_text="Endereço de e-mail",
        verbose_name="E-mail",
    )

    responsavel_tecnico = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        # help_text="Responsável técnico (apenas para clientes)",
        verbose_name="Responsável Técnico",
    )

    def __str__(self) -> str:
        return self.apelido
