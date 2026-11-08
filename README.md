# Monitor de Bolsas 🎓

[![Atualizar notícias](https://github.com/ArthurR2010/monitor-de-bolsas/actions/workflows/atualizar-noticias.yml/badge.svg)](https://github.com/ArthurR2010/monitor-de-bolsas/actions/workflows/atualizar-noticias.yml)

Projeto de aprendizado em Python para acompanhar publicações
sobre estudos e bolsas no exterior.

O programa consulta o feed RSS do Estudar Fora, organiza os
títulos e gera uma página com links para as publicações originais.

## Publicações reais

➡️ [Consultar publicações coletadas](NOTICIAS.md)

A página separa os títulos que mencionam "bolsa" ou "bolsas"
das demais publicações do feed.

**A presença na lista não confirma inscrições abertas.**
País, requisitos e prazos devem ser verificados na fonte original.

O projeto é independente e não possui vínculo com o Estudar Fora.

## Funcionalidades

- Coleta de títulos e links de um feed RSS.
- Armazenamento das publicações em JSON.
- Separação das notícias por palavras no título.
- Remoção de links duplicados na página gerada.
- Geração de uma página em Markdown.
- Atualização automática pelo GitHub Actions.
- Criação de commit automático apenas quando há alterações.
- Coleta e exibição das datas de publicação fornecidas pelo feed.
- Validação da estrutura dos links durante a coleta.
- Remoção de publicações duplicadas antes de salvar o JSON.
- Gravação temporária antes de substituir o arquivo de dados.
- Testes automáticos de links, datas, extração e gravação.
- Execução dos testes antes da coleta no GitHub Actions.

## Automação

O workflow está configurado para executar diariamente às
12h17 UTC, equivalentes a 09h17 no horário de Brasília.
O início da execução pode sofrer atrasos.

Também é possível executar manualmente:

1. Abra a aba Actions do repositório.
2. Selecione Atualizar notícias.
3. Clique em Run workflow.
4. Escolha a branch main e confirme.

A automação executa a coleta, gera a página e salva as mudanças.
Se a coleta falhar, as etapas seguintes não são executadas.

Os commits automáticos são atribuídos ao github-actions[bot].

## Como executar no computador

É necessário ter Python 3 instalado.
Os scripts usam apenas bibliotecas que acompanham o Python.

Primeiro, colete as publicações:

```bash
python coletar_noticias.py
```

Se a coleta terminar com sucesso, gere a página:

```bash
python gerar_noticias.py
```

O resultado será salvo em NOTICIAS.md.

## Testes

Para executar os testes no computador:

```bash
python -m unittest discover -v
```

Os testes usam dados fictícios, não acessam a internet e não
alteram os arquivos de publicações do projeto.

Na automação, uma falha nos testes interrompe a execução
antes da coleta.

## Estrutura do projeto

| Arquivo | Função |
| --- | --- |
| coletar_noticias.py | Consulta o feed e salva as publicações |
| noticias.json | Armazena os títulos e links coletados |
| gerar_noticias.py | Organiza as publicações e gera a página |
| NOTICIAS.md | Apresenta as publicações reais |
| .github/workflows/atualizar-noticias.yml | Configura a automação |
| main.py | Consulta exemplos fictícios pelo terminal |
| bolsas.json | Armazena bolsas fictícias para aprendizado |
| gerar_tabela.py | Gera a tabela dos exemplos fictícios |
| BOLSAS.md | Exibe a tabela dos exemplos fictícios |

## Exemplos de aprendizado

A primeira etapa do projeto utiliza bolsas fictícias para
praticar leitura de JSON, filtros por país e formatação de datas.

Para consultar esses exemplos:

```bash
python main.py
```

Para atualizar a tabela dos exemplos:

```bash
python gerar_tabela.py
```

➡️ [Ver tabela de exemplos fictícios](BOLSAS.md)

Esses exemplos não são oportunidades reais e não fazem parte
da coleta automática.

## Limitações atuais

- A coleta utiliza apenas uma fonte.
- O feed pode disponibilizar somente parte das publicações do site.
- O filtro considera apenas as palavras "bolsa" e "bolsas" no título.
- O programa ainda não identifica país ou prazo de inscrição.
- A lista não confirma a disponibilidade das oportunidades.
- Os arquivos mostram a última coleta salva com sucesso.
- Mudanças na fonte podem exigir ajustes no coletor.

## Próximas melhorias

- Melhorar a identificação de conteúdos sobre bolsas.
- Adicionar oportunidades com país e prazo verificados.
- Ampliar a cobertura de fontes.

## Aprendizados

Este projeto aplica Python, JSON, XML/RSS, expressões regulares,
tratamento de erros, Git, GitHub e GitHub Actions.

Desenvolvido por Arthur Rodrigues, com assistência de IA
na construção e explicação do código.
