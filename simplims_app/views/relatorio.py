from django.views import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from weasyprint import HTML

from django.conf import settings
import os as system_os

from ..models.ordem_servico import OrdemServico
from .ordem_servico import OrdemServicoAnaliseMixin


class OrdemServicoRelatorioPDFView(OrdemServicoAnaliseMixin, View):

    def get(self, request, pk):
        os_obj = get_object_or_404(OrdemServico, pk=pk)  # ← seguro

        analise_os = self.montar_analise(os_obj)

        # Caminho absoluto fisico da logo
        logo_path = system_os.path.join(settings.BASE_DIR, "static", "acme.png")

        html = render_to_string(
            "relatorios/relatorio_os_pdf.html",
            {
                "os": os_obj,
                "analise_os": analise_os,
                "logo_path": logo_path,
            }
        )

        pdf = HTML(string=html).write_pdf()

        return HttpResponse(pdf, content_type="application/pdf")
