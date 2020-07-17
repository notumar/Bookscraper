import requests
from bs4 import BeautifulSoup
import sqlite3


def scrape_books(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.findAll("article")

    booklist = []
    for book in books:
        # # title = book.find("h3").find("a")["title"]
        # price = float(book.select(".price_color")[0].get_text().strip("Â £"))
        # # rating = book.find("div").findNextSibling()["class"][-1]

        title = get_title(book)
        price = get_price(book)
        rating = get_rating(book)
        book_data = (title, price, rating)

        booklist.append(book_data)

    save_books(booklist)


def save_books(booklist):
    connection = sqlite3.connect("library.db/;'")
    c = connection.cursor()
    c.execute('''CREATE TABLE books (title TEXT, price REAL, rating INTEGER)''')
    c.executemany(
        "INSERT INTO books VALUES(?,?,?)", booklist)
    connection.commit()
    connection.close()


def get_title(book):
    return book.find("h3").find("a")["title"]


def get_price(book):
    return float(book.select(".price_color")[0].get_text().strip("Â £"))


def get_rating(book):
    ratings = {"One": 1, "Two": 2, "Three": 3,
               "Four": 4, "Five": 5}
    rating = book.find("div").findNextSibling()["class"][-1]
    return ratings[rating]


scrape_books(
    "http://books.toscrape.com/catalogue/category/books/history_32/index.html")
