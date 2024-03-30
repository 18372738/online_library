import os
from urllib.parse import urljoin, urlsplit, unquote

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename




def get_catalog_books(number_book, folder='books/'):
    os.makedirs(folder, exist_ok=True)
    for id in range(1, 11):
        url = f"https://tululu.org/txt.php?id={number_book}"
        response = requests.get(url)
        response.raise_for_status()
        try:
          check_for_redirect(response)
          path = download_txt(number_book)
          with open(path, 'wb') as file:
              file.write(response.content)
        except requests.exceptions.HTTPError:
          print(f'Ссылка {url} не содержит книги для скачивания.')


def get_author_and_title(number_book):
    url = f'https://tululu.org/b{number_book}/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_and_author = soup.find('div',       id='content').find('h1').text.split('::')
    author = sanitize_filename(title_and_author[-1].strip())
    title = sanitize_filename(title_and_author[0].strip())
    return author, title


def download_txt(number_book, folder='books/'):
    author, title = get_author_and_title(number_book)
    filename = f"{title}.txt"
    path = os.path.join(folder, filename)
    return(path)


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def get_image_url(number_book):
  url = f'https://tululu.org/b{number_book}/'
  response = requests.get(url)
  response.raise_for_status()
  try:
      check_for_redirect(response)
      soup = BeautifulSoup(response.text, 'lxml')
      path_image = soup.find('div', class_='bookimage').find('img')['src']
      image_url = urljoin('https://tululu.org', path_image)
      return image_url
  except requests.exceptions.HTTPError:
      return None


def download_image(url, folder='images/'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    try:
        check_for_redirect(response)
        path = urlsplit(url)
        filename = unquote(path.path).split('/')[-1]
        path = os.path.join(folder, filename)
        with open(path, 'wb') as file:
            file.write(response.content)
    except requests.exceptions.HTTPError:
        return None


if __name__ == "__main__":
    for number_book in range(1, 11):
        get_catalog_books(number_book)
        url = get_image_url(number_book)
        if url:
            download_image(url)
