import json
import os

from dotenv import load_dotenv
from livereload import Server
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape


def rebuild():
    load_dotenv()
    meta_data = os.getenv("META_DATA", "meta_data.json")
    os.makedirs("./pages", exist_ok=True)
    with open(meta_data, "r", encoding="utf8") as my_file:
        books = json.load(my_file)

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template("template.html")
    books_on_page = 10
    books_pages = list(chunked(books, books_on_page))
    for number, book_page in enumerate(books_pages):
        rendered_page = template.render(
            books = book_page,
            pages_count = len(books_pages),
            current_page = number + 1
        )

        with open(f"./pages/index-{number+1}.html", "w", encoding="utf8") as file:
            file.write(rendered_page)


def main():
    rebuild()
    server = Server()
    server.watch("template.html", rebuild)
    server.serve(root=".", default_filename="./pages/index-1.html")


if __name__ == "__main__":
    main()