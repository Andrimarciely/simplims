from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date

from simplims_app.models import OrdemServico, Empresa


class OrdemServicoModelTest(TestCase):

    def setUp(self):
        # Criar uma empresa cliente para o FK
        self.empresa = Empresa.objects.create(
            apelido="ClienteX",
            razao_social="Cliente X LTDA",
            endereco="Rua Teste, 123",
            telefone="(92) 99999-9999",
            cnpj="00.111.222/0001-33",
            tipo_empresa="CLIENTE",
            email="cliente@x.com",
            responsavel_tecnico="Fulano",
        )

    def test_criacao_basica(self):
        os = OrdemServico.objects.create(
            empresa=self.empresa,
            observacoes="Teste de OS"
        )

        self.assertIsNotNone(os.pk)
        self.assertEqual(os.empresa, self.empresa)
        self.assertEqual(os.observacoes, "Teste de OS")

        # data_emissao deve ter sido preenchida automaticamente
        self.assertEqual(os.data_emissao, date.today())

    def test_str_da_ordem_servico(self):
        os = OrdemServico.objects.create(
            empresa=self.empresa
        )
        self.assertEqual(str(os), f"OS {os.id} - {self.empresa}")

    def test_observacoes_pode_ser_vazio(self):
        os = OrdemServico.objects.create(
            empresa=self.empresa,
            observacoes=""
        )

        # deve ser válido
        self.assertEqual(os.observacoes, "")

    def test_ordenacao_default(self):
        os1 = OrdemServico.objects.create(empresa=self.empresa)
        os2 = OrdemServico.objects.create(empresa=self.empresa)

        # ordering: mais recente primeiro
        ordens = list(OrdemServico.objects.all())
        self.assertEqual(ordens[0], os2)
        self.assertEqual(ordens[1], os1)
