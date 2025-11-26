# seu_app/tests/test_models_empresa.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from ..models import Empresa


class EmpresaModelTest(TestCase):

    def setUp(self):
        # Dados válidos para criação
        self.data = {
            "apelido": "ACME",
            "razao_social": "ACME Ambiental LTDA",
            "endereco": "Rua Exemplo, 123",
            "telefone": "(92) 99999-9999",
            "cnpj": "12.345.678/0001-90",
            "tipo_empresa": "CLIENTE",
            "email": "contato@acme.com",
            "responsavel_tecnico": "Eng. João Silva",
        }

    def test_criacao_basica(self):
        empresa = Empresa.objects.create(**self.data)
        self.assertIsNotNone(empresa.pk)
        self.assertEqual(Empresa.objects.count(), 1)
        self.assertEqual(empresa.apelido, "ACME")
        self.assertEqual(empresa.razao_social, "ACME Ambiental LTDA")

    def test_str_retorna_apelido(self):
        empresa = Empresa.objects.create(**self.data)
        self.assertEqual(str(empresa), "ACME")

    def test_campos_obrigatorios(self):
        """Testa se falta de campos obrigatórios dispara ValidationError via full_clean()."""
        obrigatorios = ["apelido", "razao_social", "endereco",
                        "telefone", "cnpj", "tipo_empresa"]

        for campo in obrigatorios:
            dados = self.data.copy()
            dados[campo] = ""  # força campo em branco
            empresa = Empresa(**dados)

            with self.assertRaises(ValidationError):
                empresa.full_clean()

    def test_tipo_empresa_choices(self):
        """Valores fora das choices devem gerar ValidationError em full_clean()."""
        dados = self.data.copy()
        dados["tipo_empresa"] = "INVALIDO"
        empresa = Empresa(**dados)

        with self.assertRaises(ValidationError):
            empresa.full_clean()

    def test_email_pode_ser_vazio(self):
        dados = self.data.copy()
        dados["email"] = ""
        empresa = Empresa(**dados)
        try:
            empresa.full_clean()
        except ValidationError:
            self.fail("Email vazio deveria ser permitido.")

    def test_responsavel_tecnico_pode_ser_nulo(self):
        dados = self.data.copy()
        dados["responsavel_tecnico"] = None
        empresa = Empresa.objects.create(**dados)
        self.assertIsNone(empresa.responsavel_tecnico)

    def test_atualizar_empresa(self):
        empresa = Empresa.objects.create(**self.data)
        empresa.telefone = "(92) 98888-7777"
        empresa.save()
        empresa.refresh_from_db()
        self.assertEqual(empresa.telefone, "(92) 98888-7777")

    def test_excluir_empresa(self):
        empresa = Empresa.objects.create(**self.data)
        pk = empresa.pk
        empresa.delete()
        with self.assertRaises(Empresa.DoesNotExist):
            Empresa.objects.get(pk=pk)
