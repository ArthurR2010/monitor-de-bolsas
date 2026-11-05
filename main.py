import json
from pathlib import Path

# Localiza o arquivo de dados na pasta do programa.
arquivo = Path(__file__).parent / "bolsas.json"

# Converte os dados do JSON em uma lista do Python.
with arquivo.open("r", encoding="utf-8") as documento:
    bolsas = json.load(documento)

print("MONITOR DE BOLSAS\n")

# Mostra as informações de cada bolsa.
for bolsa in bolsas:
    print(f"Bolsa: {bolsa['nome']}")
    print(f"País: {bolsa['pais']}")
    print(f"Prazo: {bolsa['prazo']}")
    print("-" * 30)