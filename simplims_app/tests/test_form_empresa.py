from django.test import TestCase
from ..forms import EmpresaForm


class EmpresaFormTest(TestCase):

    def setUp(self):
        # Dados válidos para facilitar os testes
        self.valid_data = {
            "apelido": "ACME",
            "razao_social": "ACME Ambiental LTDA",
            "endereco": "Rua Exemplo, 123",
            "telefone": "(92) 99999-9999",
            "cnpj": "12.345.678/0001-90",
            "tipo_empresa": "CLIENTE",
            "email": "contato@acme.com",
            "responsavel_tecnico": "Eng. João Silva",
        }

    # -------------------------------
    # FORMULÁRIO VÁLIDO
    # -------------------------------
    def test_form_valido(self):
        form = EmpresaForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    # -------------------------------
    # CAMPOS OBRIGATÓRIOS
    # -------------------------------
    def test_campos_obrigatorios(self):
        obrigatorios = [
            "apelido",
            "razao_social",
            "endereco",
            "telefone",
            "cnpj",
            "tipo_empresa",
        ]

        for campo in obrigatorios:
            dados = self.valid_data.copy()
            dados[campo] = ""  # esvazia campo obrigatório

            form = EmpresaForm(data=dados)
            self.assertFalse(form.is_valid(), f"O campo {campo} deveria ser obrigatório.")
            self.assertIn(campo, form.errors)

    # -------------------------------
    # CAMPO EMAIL OPCIONAL
    # -------------------------------
    def test_email_pode_ser_vazio(self):
        dados = self.valid_data.copy()
        dados["email"] = ""

        form = EmpresaForm(data=dados)
        self.assertTrue(form.is_valid())

    # -------------------------------
    # RESPONSÁVEL TÉCNICO OPCIONAL
    # -------------------------------
    def test_responsavel_tecnico_pode_ser_vazio(self):
        dados = self.valid_data.copy()
        dados["responsavel_tecnico"] = ""

        form = EmpresaForm(data=dados)
        self.assertTrue(form.is_valid())

    # -------------------------------
    # VALIDAÇÃO DE choices
    # -------------------------------
    def test_tipo_empresa_invalido(self):
        dados = self.valid_data.copy()
        dados["tipo_empresa"] = "INVALIDO"

        form = EmpresaForm(data=dados)
        self.assertFalse(form.is_valid())
        self.assertIn("tipo_empresa", form.errors)

    # -------------------------------
    # FORM COM EMAIL INVÁLIDO
    # -------------------------------
    def test_form_email_invalido(self):
        dados = self.valid_data.copy()
        dados["email"] = "nao-e-email"

        form = EmpresaForm(data=dados)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
