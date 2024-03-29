import os

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename




def catalog_books(folder='books/'):
    for id in range(1, 11):
        url = f"https://tululu.org/txt.php?id={id}"
        response = requests.get(url)
        response.raise_for_status()
        try:
          check_for_redirect(response)
          path = download_txt(id)
          with open(path, 'wb') as file:
              file.write(response.content)
        except requests.exceptions.HTTPError:
          print(f'Ссылка {url} не содержит книги для скачивания.')


def get_author_and_title(book_number):
    url = f'https://tululu.org/b{book_number}/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_and_author = soup.find('div',       id='content').find('h1').text.split('::')
    author = sanitize_filename(title_and_author[-1].strip())
    title = sanitize_filename(title_and_author[0].strip())
    return author, title


def download_txt(book_number, folder='books/'):
    author, title = get_author_and_title(book_number)
    filename = f"{title}.txt"
    path = os.path.join(folder, filename)
    return(path)

def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError




if __name__ == "__main__":
    os.makedirs('books', exist_ok=True)
    catalog_books()
   
