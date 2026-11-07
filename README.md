# Monitor de Bolsas

Projeto de aprendizado em Python para organizar oportunidades
de bolsas de estudo.

## Funcionalidades atuais

## Funcionalidades atuais

- Leitura de dados de um arquivo JSON.
- Exibição do nome, país e prazo de cada oportunidade no terminal.
- Apresentação das datas no formato brasileiro.
- Filtro por país, sem diferenciar maiúsculas de minúsculas.
- Contagem das oportunidades encontradas.
- Geração de uma tabela em Markdown, ordenada por prazo.

Os dados atuais são fictícios e servem apenas para testes.
O programa ainda não busca oportunidades na internet.

## Como executar

É necessário ter Python 3 instalado.

No terminal, dentro da pasta do projeto, execute:

```bash
python main.py
```

## Tabela de oportunidades

Veja a [tabela de bolsas](BOLSAS.md).

Para gerar ou atualizar a tabela a partir do JSON, execute:

```bash
python gerar_tabela.py
```

Os dados apresentados ainda são fictícios.

## Coleta de publicações reais

O projeto consulta o feed RSS do Estudar Fora e salva
títulos, links e fonte no arquivo noticias.json.

Para executar:

```bash
python coletar_noticias.py
```

As publicações podem incluir notícias e orientações gerais.
A coleta ainda não identifica país, prazo de inscrição
ou se uma bolsa está aberta.

O arquivo bolsas.json e a tabela BOLSAS.md continuam
utilizando dados fictícios para testes.

## Página de publicações

Veja as [publicações coletadas do Estudar Fora](NOTICIAS.md).

Para atualizar os dados da fonte, execute:

```bash
python coletar_noticias.py
```

Se a coleta terminar com sucesso, gere a página:

```bash
python gerar_noticias.py
```

A página separa títulos que mencionam "bolsa" ou "bolsas"
das outras publicações do feed.

Esse filtro não confirma inscrições abertas.
País, requisitos e prazos devem ser consultados na fonte original.

Os dados reais ficam em noticias.json e NOTICIAS.md.
Os arquivos bolsas.json e BOLSAS.md continuam com exemplos fictícios.

## Próximas melhorias

- Consultar uma fonte real e automatizar as atualizações.

## Desenvolvimento

Projeto desenvolvido como prática de programação,
com assistência de IA na construção e explicação do código.