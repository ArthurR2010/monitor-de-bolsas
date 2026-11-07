import json
import sys
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

URL_FEED = "https://www.estudarfora.org.br/feed/"

pasta = Path(__file__).parent
arquivo_saida = pasta / "noticias.json"

requisicao = Request(
    URL_FEED,
    headers={
        "User-Agent": "MonitorDeBolsas/0.1 (projeto educacional)",
        "Accept": "application/rss+xml, application/xml, text/xml",
    },
)

try:
    print("Consultando publicações do Estudar Fora...")

    with urlopen(requisicao, timeout=30) as resposta:
        dados_xml = resposta.read()

    raiz = ET.fromstring(dados_xml)
    noticias = []

    for item in raiz.findall("./channel/item"):
        titulo = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        data_original = (item.findtext("pubDate") or "").strip()

        # Datas ausentes ou inválidas ficam como null no JSON.
        publicado_em = None

        if data_original:
            try:
                data = parsedate_to_datetime(data_original)
                publicado_em = data.isoformat()
            except (ValueError, TypeError, OverflowError):
                print(f"Data não reconhecida: {titulo}")

        if titulo and link:
            noticias.append({
                "titulo": titulo,
                "link": link,
                "fonte": "Estudar Fora",
                "publicado_em": publicado_em,
            })

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

    print(f"Publicações coletadas: {len(noticias)}")
    print(f"Arquivo salvo: {arquivo_saida.name}")

except (HTTPError, URLError, TimeoutError, ET.ParseError, ValueError) as erro:
    print(f"Não foi possível concluir a coleta: {erro}")
    print("Os dados anteriores foram preservados.")
    sys.exit(1)
