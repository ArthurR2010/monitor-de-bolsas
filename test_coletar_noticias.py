import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch

from coletar_noticias import (
    converter_data,
    extrair_noticias,
    link_valido,
    salvar_noticias,
)


class TestColetor(unittest.TestCase):
    def test_links_validos(self):
        for link in (
            "https://example.com/bolsas",
            "http://example.com/noticia",
        ):
            with self.subTest(link=link):
                self.assertTrue(link_valido(link))

    def test_links_invalidos(self):
        for link in (
            "",
            None,
            "/pagina-local",
            "https://",
            "javascript:alert(1)",
            "https://example.com/com espaco",
            "https://[",
        ):
            with self.subTest(link=link):
                self.assertFalse(link_valido(link))

    def test_converte_data_rss(self):
        resultado = converter_data(
            "Sun, 08 Nov 2026 12:00:00 +0000"
        )

        self.assertEqual(
            resultado,
            "2026-11-08T12:00:00+00:00",
        )

    def test_datas_ausentes_ou_invalidas(self):
        for texto in ("", None, "data desconhecida"):
            with self.subTest(texto=texto):
                self.assertIsNone(converter_data(texto))

    def test_extracao_descarta_invalidos_e_duplicatas(self):
        xml = """
        <rss>
          <channel>
            <item>
              <title> Bolsa de teste </title>
              <link>https://example.com/bolsa</link>
            </item>
            <item>
              <title>Publicação duplicada</title>
              <link>https://example.com/bolsa</link>
            </item>
            <item>
              <link>https://example.com/sem-titulo</link>
            </item>
            <item>
              <title>Link inválido</title>
              <link>/pagina-local</link>
            </item>
          </channel>
        </rss>
        """

        noticias, descartadas = extrair_noticias(xml)

        self.assertEqual(len(noticias), 1)
        self.assertEqual(descartadas, 3)
        self.assertEqual(noticias[0]["titulo"], "Bolsa de teste")
        self.assertIsNone(noticias[0]["publicado_em"])

    def test_feed_sem_registros_validos(self):
        with self.assertRaises(ValueError):
            extrair_noticias("<rss><channel /></rss>")

    def test_xml_malformado(self):
        with self.assertRaises(ET.ParseError):
            extrair_noticias("<rss>")

    def test_gravacao_do_json(self):
        noticias = [{
            "titulo": "Bolsa de teste",
            "link": "https://example.com/bolsa",
            "fonte": "Teste",
            "publicado_em": None,
        }]

        with tempfile.TemporaryDirectory() as pasta:
            destino = Path(pasta) / "noticias.json"
            salvar_noticias(noticias, destino)

            resultado = json.loads(
                destino.read_text(encoding="utf-8")
            )

            self.assertEqual(resultado, noticias)
            self.assertFalse(
                destino.with_suffix(".json.tmp").exists()
            )

    def test_falha_na_gravacao_preserva_arquivo_anterior(self):
        with tempfile.TemporaryDirectory() as pasta:
            destino = Path(pasta) / "noticias.json"
            conteudo_anterior = '[{"titulo": "Anterior"}]\n'
            destino.write_text(conteudo_anterior, encoding="utf-8")

            with patch.object(
                Path,
                "write_text",
                side_effect=OSError("Falha simulada"),
            ):
                with self.assertRaises(OSError):
                    salvar_noticias([], destino)

            self.assertEqual(
                destino.read_text(encoding="utf-8"),
                conteudo_anterior,
            )


if __name__ == "__main__":
    unittest.main()
