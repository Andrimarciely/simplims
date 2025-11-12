"""
Mixins genéricos para usar com as views
"""


class DeleteRecordMixin:
    """
    Mixin para adicionar lógica extra em DeleteView (mensagens, logs, etc.)
    """

    def post(self, request, *args, **kwargs):
        # Aqui você pode adicionar lógica comum, como log ou mensagens
        # print(f"Registro será deletado: {self.object}") <- aqui não existe object!
        success_message = "Registro excluído com sucesso."
        return super().delete(request, *args, **kwargs)
