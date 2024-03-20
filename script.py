import os

import requests


def catalog_books():
    id = 0
    for id in range(10):
        id += 1
        url = f"https://tululu.org/txt.php?id={id}"
        response = requests.get(url)
        response.raise_for_status()
        with open(f"books/id{id}.txt", 'wb') as file:
            file.write(response.content)


if __name__ == "__main__":
    os.makedirs('books', exist_ok=True)
    catalog_books()
