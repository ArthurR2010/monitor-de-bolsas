import json
from datetime import date
from pathlib import Path

# Localiza a pasta do projeto.
pasta = Path(__file__).parent
arquivo_dados = pasta / "bolsas.json"
arquivo_saida = pasta / "BOLSAS.md"

# Lê as bolsas cadastradas.
with arquivo_dados.open("r", encoding="utf-8") as documento:
    bolsas = json.load(documento)

# Organiza as bolsas do prazo mais próximo para o mais distante.
bolsas_ordenadas = sorted(
    bolsas,
    key=lambda bolsa: date.fromisoformat(bolsa["prazo"])
)

# Monta o cabeçalho do documento e da tabela.
linhas = [
    "# Oportunidades de bolsas",
    "",
    "**Dados fictícios para testes. Não são oportunidades reais.**",
    "",
    "| Bolsa | País | Prazo |",
    "| --- | --- | --- |",
]

# Adiciona uma linha à tabela para cada bolsa.
for bolsa in bolsas_ordenadas:
    prazo = date.fromisoformat(bolsa["prazo"])
    prazo_formatado = prazo.strftime("%d/%m/%Y")

    linha = (
        f"| {bolsa['nome']} "
        f"| {bolsa['pais']} "
        f"| {prazo_formatado} |"
    )

    linhas.append(linha)

# Adiciona a quantidade total abaixo da tabela.
linhas.extend([
    "",
    f"Total de oportunidades: {len(bolsas)}",
])

# Junta as linhas e grava o documento.
conteudo = "\n".join(linhas) + "\n"
arquivo_saida.write_text(conteudo, encoding="utf-8")

print(f"Tabela gerada em: {arquivo_saida.name}")
print(f"Total de oportunidades: {len(bolsas)}")