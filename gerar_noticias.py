import json
import re
from datetime import datetime
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

pasta = Path(__file__).parent
arquivo_dados = pasta / "noticias.json"
arquivo_saida = pasta / "NOTICIAS.md"

with arquivo_dados.open("r", encoding="utf-8") as documento:
    noticias = json.load(documento)

relacionadas = []
outras = []
links_vistos = set()

for noticia in noticias:
    titulo = noticia["titulo"].strip()
    link = noticia["link"].strip()

    endereco = urlsplit(link)

    if endereco.scheme not in ("http", "https") or not endereco.netloc:
        continue

    if link in links_vistos:
        continue

    links_vistos.add(link)

    if re.search(r"\bbolsas?\b", titulo, flags=re.IGNORECASE):
        relacionadas.append(noticia)
    else:
        outras.append(noticia)

linhas = [
    "# Publicações do Estudar Fora",
    "",
    "Fonte: https://www.estudarfora.org.br/",
    "",
    "O filtro usa apenas o título e não confirma inscrições abertas.",
    "As datas abaixo são de publicação, não prazos de inscrição.",
    "Confira país, requisitos e prazo na publicação original.",
    "",
]

grupos = [
    ("Títulos que mencionam bolsas", relacionadas),
    ("Outras publicações do feed", outras),
]

for nome_grupo, publicacoes in grupos:
    linhas.extend([f"## {nome_grupo}", ""])

    if not publicacoes:
        linhas.extend(["Nenhuma publicação neste grupo.", ""])
        continue

    for noticia in publicacoes:
        titulo = escape(" ".join(noticia["titulo"].split()))
        link = escape(noticia["link"].strip(), quote=True)

        data_formatada = "Não informada"
        publicado_em = noticia.get("publicado_em")

        if publicado_em:
            try:
                data = datetime.fromisoformat(publicado_em)
                data_formatada = data.strftime("%d/%m/%Y")
            except (ValueError, TypeError):
                data_formatada = "Não reconhecida"

        linhas.append(
            f'- <a href="{link}">{titulo}</a>'
            f" — Publicação: {data_formatada}"
        )

    linhas.append("")

total = len(relacionadas) + len(outras)
linhas.append(f"Total de publicações listadas: {total}")

conteudo = "\n".join(linhas) + "\n"
arquivo_saida.write_text(conteudo, encoding="utf-8")

print(f"Página gerada: {arquivo_saida.name}")
print(f"Total de publicações: {total}")
