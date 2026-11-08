import json
import sys
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

URL_FEED = "https://www.estudarfora.org.br/feed/"


def link_valido(link):
    """Verifica o formato do endereço sem acessar a internet."""
    if not isinstance(link, str):
        return False

    try:
        endereco = urlsplit(link)

        return (
            endereco.scheme in ("http", "https")
            and bool(endereco.hostname)
            and not any(caractere.isspace() for caractere in link)
        )
    except ValueError:
        return False


def converter_data(texto):
    """Converte uma data RSS para ISO; retorna None se inválida."""
    if not texto:
        return None

    try:
        return parsedate_to_datetime(texto).isoformat()
    except (ValueError, TypeError, OverflowError):
        return None


def extrair_noticias(dados_xml):
    """Lê o XML, valida os registros e remove links repetidos."""
    raiz = ET.fromstring(dados_xml)
    noticias = []
    links_vistos = set()
    descartadas = 0

    for item in raiz.findall("./channel/item"):
        titulo = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        data_original = (item.findtext("pubDate") or "").strip()

        if not titulo or not link_valido(link):
            descartadas += 1
            continue

        if link in links_vistos:
            descartadas += 1
            continue

        links_vistos.add(link)

        noticias.append({
            "titulo": titulo,
            "link": link,
            "fonte": "Estudar Fora",
            "publicado_em": converter_data(data_original),
        })

    if not noticias:
        raise ValueError("Nenhuma publicação válida encontrada.")

    return noticias, descartadas


def salvar_noticias(noticias, arquivo_saida):
    """Substitui o JSON após concluir a gravação temporária."""
    conteudo = json.dumps(
        noticias,
        ensure_ascii=False,
        indent=2,
    )

    temporario = arquivo_saida.with_suffix(".json.tmp")
    temporario.write_text(conteudo + "\n", encoding="utf-8")
    temporario.replace(arquivo_saida)


def main():
    arquivo_saida = Path(__file__).parent / "noticias.json"

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

        noticias, descartadas = extrair_noticias(dados_xml)
        salvar_noticias(noticias, arquivo_saida)

        print(f"Publicações válidas: {len(noticias)}")
        print(f"Registros descartados: {descartadas}")
        print(f"Arquivo salvo: {arquivo_saida.name}")

    except (
        HTTPError,
        URLError,
        TimeoutError,
        ET.ParseError,
        ValueError,
    ) as erro:
        print(f"Falha na coleta: {erro}")
        print("Os dados anteriores foram preservados.")
        return 1

    except OSError as erro:
        print(f"Falha ao acessar ou salvar os arquivos: {erro}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
