import json
import sys
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

URL_FEED = "https://www.estudarfora.org.br/feed/"

pasta = Path(__file__).parent
arquivo_saida = pasta / "noticias.json"


def link_valido(link):
    """Verifica a estrutura do link, sem acessar a página."""
    try:
        endereco = urlsplit(link)

        return (
            endereco.scheme in ("http", "https")
            and bool(endereco.hostname)
            and not any(caractere.isspace() for caractere in link)
        )
    except ValueError:
        return False


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
    links_vistos = set()
    descartadas = 0

    for item in raiz.findall("./channel/item"):
        titulo = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        data_original = (item.findtext("pubDate") or "").strip()

        # Ignora registros incompletos ou com links inválidos.
        if not titulo or not link_valido(link):
            descartadas += 1
            continue

        # Evita salvar o mesmo link mais de uma vez.
        if link in links_vistos:
            descartadas += 1
            continue

        links_vistos.add(link)

        publicado_em = None

        if data_original:
            try:
                data = parsedate_to_datetime(data_original)
                publicado_em = data.isoformat()
            except (ValueError, TypeError, OverflowError):
                print(f"Data não reconhecida: {titulo}")

        noticias.append({
            "titulo": titulo,
            "link": link,
            "fonte": "Estudar Fora",
            "publicado_em": publicado_em,
        })

    if not noticias:
        raise ValueError(
            "Nenhuma publicação válida encontrada. "
            "O formato do feed pode ter mudado."
        )

    conteudo = json.dumps(
        noticias,
        ensure_ascii=False,
        indent=2,
    )

    # Grava primeiro em um arquivo temporário.
    arquivo_temporario = arquivo_saida.with_suffix(".json.tmp")
    arquivo_temporario.write_text(
        conteudo + "\n",
        encoding="utf-8",
    )

    # Substitui o JSON anterior depois da gravação completa.
    arquivo_temporario.replace(arquivo_saida)

    print(f"Publicações válidas: {len(noticias)}")
    print(f"Registros descartados: {descartadas}")
    print(f"Arquivo salvo: {arquivo_saida.name}")

except (HTTPError, URLError, TimeoutError, ET.ParseError, ValueError) as erro:
    print(f"Não foi possível concluir a coleta: {erro}")
    print("Os dados anteriores foram preservados.")
    sys.exit(1)

except OSError as erro:
    print(f"Falha ao acessar ou salvar os arquivos: {erro}")
    sys.exit(1)
