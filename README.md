# Web Scraping com Python - EBAC

Este projeto é um exercício prático de web scraping desenvolvido no curso da EBAC. O script utiliza bibliotecas como `requests`, `BeautifulSoup` e `concurrent.futures` para extrair informações de filmes populares do site IMDb e salvar os dados em um arquivo CSV.

## Funcionalidades

- Extrai os **15 filmes mais populares** da página do IMDb.
- Coleta informações como:
  - Título do filme
  - Data de lançamento
  - Classificação
  - Sinopse
- Salva os dados em um arquivo `movies.csv`.

## Tecnologias Utilizadas

- Python
  - `requests`
  - `BeautifulSoup`
  - `csv`
  - `concurrent.futures`

## Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/rafaelscdev/webScraping.git
