import os
from urllib.parse import urljoin, urlsplit, unquote
import argparse

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename




def parse_book_page(soup, url):
    title_and_author = soup.find('div', id='content').find('h1').text.split('::')
    author = sanitize_filename(title_and_author[-1].strip())
    title = sanitize_filename(title_and_author[0].strip())
    path_image = soup.find('div', class_='bookimage').find('img')['src']
    image_url = urljoin(url, path_image)
    text_comments = soup.find('div', id='content').find_all('span', class_='black')
    comments = []
    for comment in text_comments:
          comments.append(comment.text)
    text_genres = soup.find('span', class_='d_book').find_all('a')
    genres = []
    for genre in text_genres:
        genres.append(genre.text)
    book = {
        'title': title,
        'author': author,
        'genres': genres,
        'image_url': image_url,
        'comments': comments,
        }
    return book


def download_txt(content, title, folder='books/'):
    os.makedirs(folder, exist_ok=True)
    filename = f"{title}.txt"
    path = os.path.join(folder, filename)
    with open(path, 'wb') as file:
        file.write(content)
    return(path)


def download_image(content, url, folder='images/'):
    os.makedirs(folder, exist_ok=True)
    path = urlsplit(url)
    filename = unquote(path.path).split('/')[-1]
    path = os.path.join(folder, filename)
    with open(path, 'wb') as file:
        file.write(content)


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


if __name__ == "__main__":
    url_template = "https://tululu.org/b"
    parser = argparse.ArgumentParser(description='Скачивает книги с сайта tululu.org.')
    parser.add_argument('--first', default=1, type=int, help='id первой книги для скачивания.')
    parser.add_argument('--last', default=10, type=int, help='id последней книги для скачивания.')
    args = parser.parse_args()
    number_first_book = args.first
    number_last_book = args.last + 1
    for number_book in range(number_first_book, number_last_book):
        url = f"{url_template}{number_book}/"
        response = requests.get(url)
        response.raise_for_status()
        try:
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')
            book = parse_book_page(soup, url)

            title = book['title']
            download_book_url = f"https://tululu.org/txt.php?id={number_book}"
            response = requests.get(download_book_url)
            response.raise_for_status()
            check_for_redirect(response)
            download_txt(response.content, title)

            image_url = book['image_url']
            response = requests.get(image_url)
            response.raise_for_status()
            download_image(response.content, image_url)
        except requests.exceptions.HTTPError:
                print(f'По ссылке {url} книга не найдена.')
