# simplims_app/tests/test_integracao_empresa.py

from django.test import TestCase
from django.urls import reverse
from ..models import Empresa


class EmpresaIntegracaoTest(TestCase):

    def test_fluxo_completo_empresa(self):
        """
        Teste de integração que valida todo o ciclo de vida da entidade Empresa:
        criar -> listar -> editar -> excluir.
        """

        # ---------------------------------------
        # 1. ACESSAR FORMULÁRIO DE CRIAÇÃO (GET)
        # ---------------------------------------
        url_criar = reverse("empresa_criar")
        response = self.client.get(url_criar)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "simplims_app/empresa/formulario.html")

        # ---------------------------------------
        # 2. CRIAR EMPRESA (POST)
        # ---------------------------------------
        dados_criacao = {
            "apelido": "EmpresaX",
            "razao_social": "Empresa X Ltda",
            "endereco": "Rua Teste, 100",
            "telefone": "(92) 99999-9999",
            "cnpj": "00.111.222/0001-33",
            "tipo_empresa": "CLIENTE",
            "email": "contato@empresax.com",
            "responsavel_tecnico": "Eng. Fulano",
        }

        response = self.client.post(url_criar, dados_criacao)

        # Redirecionamento após criação
        url_listar = reverse("empresa_listar")
        self.assertRedirects(response, url_listar)

        # Empresa criada no banco
        self.assertTrue(Empresa.objects.filter(apelido="EmpresaX").exists())

        empresa = Empresa.objects.get(apelido="EmpresaX")

        # ---------------------------------------
        # 3. LISTAR EMPRESAS (GET)
        # ---------------------------------------
        response = self.client.get(url_listar)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "simplims_app/empresa/lista.html")
        self.assertIn(empresa, response.context["object_list"])

        # ---------------------------------------
        # 4. ACESSAR FORM DE EDIÇÃO (GET)
        # ---------------------------------------
        url_editar = reverse("empresa_editar", args=[empresa.pk])
        response = self.client.get(url_editar)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "simplims_app/empresa/formulario.html")

        # ---------------------------------------
        # 5. EDITAR EMPRESA (POST)
        # ---------------------------------------
        dados_edicao = dados_criacao.copy()
        dados_edicao["apelido"] = "EmpresaX-Editada"

        response = self.client.post(url_editar, dados_edicao)

        self.assertRedirects(response, url_listar)

        empresa.refresh_from_db()
        self.assertEqual(empresa.apelido, "EmpresaX-Editada")

        # ---------------------------------------
        # 6. ACESSAR PÁGINA DE EXCLUSÃO (GET)
        # ---------------------------------------
        url_excluir = reverse("empresa_excluir", args=[empresa.pk])
        response = self.client.get(url_excluir)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "simplims_app/empresa/confirmar_exclusao.html")

        # ---------------------------------------
        # 7. EXCLUIR EMPRESA (POST)
        # ---------------------------------------
        response = self.client.post(url_excluir)

        self.assertRedirects(response, url_listar)

        # ---------------------------------------
        # 8. GARANTIR QUE A EMPRESA FOI REMOVIDA
        # ---------------------------------------
        self.assertFalse(Empresa.objects.filter(pk=empresa.pk).exists())
