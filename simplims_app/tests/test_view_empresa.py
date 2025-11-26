from django.test import TestCase
from django.urls import reverse
from ..models import Empresa


class EmpresaViewsTest(TestCase):
    def setUp(self):
        # Registro inicial para testes de editar e excluir
        self.empresa = Empresa.objects.create(
            apelido="ACME",
            razao_social="ACME Ambiental LTDA",
            endereco="Rua Exemplo, 123",
            telefone="(92) 99999-9999",
            cnpj="12.345.678/0001-90",
            tipo_empresa="CLIENTE",
            email="contato@acme.com",
            responsavel_tecnico="Eng. João Silva",
        )

        # URLs conforme teu urls.py
        self.url_listar = reverse("empresa_listar")
        self.url_criar = reverse("empresa_criar")
        self.url_editar = reverse("empresa_editar", args=[self.empresa.pk])
        self.url_excluir = reverse("empresa_excluir", args=[self.empresa.pk])

    # ----------------------------------
    # LISTAR EMPRESA
    # ----------------------------------
    def test_listar_empresas(self):
        response = self.client.get(self.url_listar)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "simplims_app/empresa/lista.html")

        # Empresa precisa aparecer na lista
        self.assertIn(self.empresa, response.context["object_list"])

    # ----------------------------------
    # CRIAR EMPRESA
    # ----------------------------------
    def test_criar_empresa_get(self):
        response = self.client.get(self.url_criar)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "simplims_app/empresa/formulario.html")

    def test_criar_empresa_post(self):
        data = {
            "apelido": "Nova",
            "razao_social": "Nova Empresa LTDA",
            "endereco": "Rua Nova, 999",
            "telefone": "(92) 98888-8888",
            "cnpj": "33.333.333/0001-33",
            "tipo_empresa": "CLIENTE",
            "email": "nova@empresa.com",
            "responsavel_tecnico": "Maria Silva",
        }

        response = self.client.post(self.url_criar, data)

        # Deve redirecionar para listar
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url_listar)

        # Registro foi criado:
        self.assertTrue(Empresa.objects.filter(apelido="Nova").exists())

    # ----------------------------------
    # EDITAR EMPRESA
    # ----------------------------------
    def test_editar_empresa_get(self):
        response = self.client.get(self.url_editar)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "simplims_app/empresa/formulario.html")

    def test_editar_empresa_post(self):
        data = {
            "apelido": "Alterada",
            "razao_social": self.empresa.razao_social,
            "endereco": self.empresa.endereco,
            "telefone": self.empresa.telefone,
            "cnpj": self.empresa.cnpj,
            "tipo_empresa": self.empresa.tipo_empresa,
            "email": self.empresa.email,
            "responsavel_tecnico": self.empresa.responsavel_tecnico,
        }

        response = self.client.post(self.url_editar, data)

        # Redireciona após salvar:
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url_listar)

        # Valor atualizado:
        self.empresa.refresh_from_db()
        self.assertEqual(self.empresa.apelido, "Alterada")

    # ----------------------------------
    # EXCLUIR EMPRESA
    # ----------------------------------
    def test_excluir_empresa_get(self):
        response = self.client.get(self.url_excluir)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "simplims_app/empresa/confirmar_exclusao.html")

    def test_excluir_empresa_post(self):
        response = self.client.post(self.url_excluir)

        # Redireciona após exclusão:
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url_listar)

        # Registro removido:
        self.assertFalse(Empresa.objects.filter(pk=self.empresa.pk).exists())
