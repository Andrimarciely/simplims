from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    cliente_sistema = models.ForeignKey(
        "simplims_app.ClienteSistema",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username
