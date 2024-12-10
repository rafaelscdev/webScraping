import requests
import time
import csv
import random
import concurrent.futures
from bs4 import BeautifulSoup

# Global headers para serem usados nas requisições
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}

MAX_THREADS = 10

def extract_movie_details(movie_link):
    time.sleep(random.uniform(0.5, 1.5))  # Evitar bloqueio por requisições rápidas
    response = requests.get(movie_link, headers=headers)
    movie_soup = BeautifulSoup(response.content, 'html.parser')

    if movie_soup is not None:
        title = None
        date = None
        
        # Encontrando o título do filme
        title_tag = movie_soup.find('h1')
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # Encontrando a data de lançamento
        date_tag = movie_soup.find('a', href=lambda href: href and 'releaseinfo' in href)
        if date_tag:
            date = date_tag.get_text(strip=True)
        
        # Encontrando a classificação do filme
        rating_tag = movie_soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
        rating = rating_tag.get_text(strip=True) if rating_tag else None
        
        # Encontrando a sinopse do filme
        plot_tag = movie_soup.find('span', attrs={'data-testid': 'plot-xs_to_m'})
        plot_text = plot_tag.get_text(strip=True) if plot_tag else None
        
        # Escrevendo os dados no arquivo CSV
        with open('movies.csv', mode='a', newline='', encoding='utf-8') as file:
            movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if all([title, date, rating, plot_text]):
                print(title, date, rating, plot_text)
                movie_writer.writerow([title, date, rating, plot_text])

def extract_movies(soup):
    # Localizar a lista de filmes populares
    movies_table = soup.find('div', attrs={'data-testid': 'chart-layout-main-column'}).find('ul')
    if not movies_table:
        print("Não foi possível localizar a tabela de filmes.")
        return

    # Limitar aos primeiros 15 filmes
    movies_table_rows = movies_table.find_all('li')[:16]
    movie_links = ['https://imdb.com' + movie.find('a')['href'] for movie in movies_table_rows]

    threads = min(MAX_THREADS, len(movie_links))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(extract_movie_details, movie_links)

def main():
    start_time = time.time()

    # URL da página de filmes mais populares do IMDb
    popular_movies_url = 'https://www.imdb.com/chart/moviemeter/'
    response = requests.get(popular_movies_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Criar o arquivo CSV com cabeçalhos
    with open('movies.csv', mode='w', newline='', encoding='utf-8') as file:
        movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        movie_writer.writerow(['Title', 'Release Date', 'Rating', 'Plot'])

    # Função principal para extrair os 15 filmes
    extract_movies(soup)

    end_time = time.time()
    print('Total time taken: ', end_time - start_time)

if __name__ == '__main__':
    main()
