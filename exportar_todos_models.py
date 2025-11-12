# export_all_models.py
import os
from django.apps import apps
from django.core.management import call_command

# Nome do app que você quer exportar
APP_NAME = 'simplims_app'

# Diretório onde os arquivos JSON serão salvos
FIXTURES_DIR = os.path.join(APP_NAME, 'fixtures')
os.makedirs(FIXTURES_DIR, exist_ok=True)

# Pega todos os modelos do app
app_config = apps.get_app_config(APP_NAME)
models = app_config.get_models()

for model in models:
    # Nome do arquivo baseado no nome do model
    filename = os.path.join(FIXTURES_DIR, f'{model.__name__.lower()}.json')
    print(f'Exportando {model.__name__} para {filename}...')

    # Executa dumpdata para o model específico
    with open(filename, 'w', encoding='utf-8') as f:
        call_command('dumpdata', f'{APP_NAME}.{model.__name__}', format='json', indent=2, stdout=f)

print('Exportação completa!')
