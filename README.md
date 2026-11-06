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

## Próximas melhorias

- Consultar uma fonte real e automatizar as atualizações.

## Desenvolvimento

Projeto desenvolvido como prática de programação,
com assistência de IA na construção e explicação do código.