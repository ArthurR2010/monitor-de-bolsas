import json
from datetime import date
from pathlib import Path

# Localiza o arquivo de dados na pasta do programa.
arquivo = Path(__file__).parent / "bolsas.json"

# Lê os dados do JSON.
with arquivo.open("r", encoding="utf-8") as documento:
    bolsas = json.load(documento)

print("MONITOR DE BOLSAS")
print("Dados fictícios para testes.\n")

# Permite pesquisar um país ou mostrar todas as bolsas.
pais_desejado = input(
    "Digite um país ou pressione Enter para ver todas: "
).strip()

quantidade = 0

for bolsa in bolsas:
    # Ignora bolsas de outros países quando há um filtro.
    if pais_desejado and (
        bolsa["pais"].casefold() != pais_desejado.casefold()
    ):
        continue

    # Converte a data do JSON para o formato brasileiro.
    prazo = date.fromisoformat(bolsa["prazo"])
    prazo_formatado = prazo.strftime("%d/%m/%Y")

    print()
    print(f"Bolsa: {bolsa['nome']}")
    print(f"País: {bolsa['pais']}")
    print(f"Prazo: {prazo_formatado}")
    print("-" * 30)

    quantidade += 1

if quantidade == 0:
    print("\nNenhuma bolsa encontrada para esse país.")
else:
    print(f"\nTotal de bolsas encontradas: {quantidade}")