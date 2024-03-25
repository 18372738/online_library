import os

import requests


def catalog_books():
    for id in range(1, 11):
        url = f"https://tululu.org/txt.php?id={id}"
        response = requests.get(url)
        response.raise_for_status()
        try:
            check_for_redirect(response)
            with open(f"books/id{id}.txt", 'wb') as file:
                file.write(response.content)
        except requests.exceptions.HTTPError:
          print(f'Ссылка {url} не содержит книги для скачивания.')

def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError



if __name__ == "__main__":
    os.makedirs('books', exist_ok=True)
    catalog_books()
