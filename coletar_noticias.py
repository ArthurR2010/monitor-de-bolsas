import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

URL_FEED = "https://www.estudarfora.org.br/feed/"

pasta = Path(__file__).parent
arquivo_saida = pasta / "noticias.json"

# Identifica o programa que está fazendo a consulta.
requisicao = Request(
    URL_FEED,
    headers={
        "User-Agent": "MonitorDeBolsas/0.1 (projeto educacional)",
        "Accept": "application/rss+xml, application/xml, text/xml",
    },
)

try:
    print("Consultando publicações do Estudar Fora...")

    # Faz uma consulta com limite de espera de 30 segundos.
    with urlopen(requisicao, timeout=30) as resposta:
        dados_xml = resposta.read()

    # Interpreta a estrutura XML do feed RSS.
    raiz = ET.fromstring(dados_xml)

    noticias = []

    for item in raiz.findall("./channel/item"):
        titulo = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()

        if titulo and link:
            noticias.append({
                "titulo": titulo,
                "link": link,
                "fonte": "Estudar Fora",
            })

    # Não substitui o arquivo anterior se a coleta vier vazia.
    if not noticias:
        raise ValueError(
            "Nenhuma publicação encontrada. "
            "O formato do feed pode ter mudado."
        )

    conteudo = json.dumps(
        noticias,
        ensure_ascii=False,
        indent=2,
    )

    arquivo_saida.write_text(conteudo + "\n", encoding="utf-8")

    print(f"\nPublicações coletadas: {len(noticias)}")
    print(f"Arquivo salvo: {arquivo_saida.name}")

    print("\nPrimeiras publicações:")

    for noticia in noticias[:5]:
        print(f"\nTítulo: {noticia['titulo']}")
        print(f"Link: {noticia['link']}")

except (HTTPError, URLError, TimeoutError, ET.ParseError, ValueError) as erro:
    print(f"\nNão foi possível concluir a coleta: {erro}")
    print("Os dados anteriores foram preservados.")
    sys.exit(1)