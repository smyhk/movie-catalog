import sys
import os
import sqlite3
from contextlib import closing

from objects import Movie
from objects import Category


conn = None  # global (not sure why, yet)


def connect():
    global conn
    if not conn:
        if sys.platform == "win32":
            DB_FILE = "movies.sqlite"  # path to file
        else:
            HOME = os.environ["HOME"]
            DB_FILE = "movies.sqlite"  # append HOME to path (Unix, Mac, Linux
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row


def close():
    if conn:
        conn.close()


def make_category(row):
    return Category(row["categoryID"], row["categoryName"])


def make_movie(row):
    return Movie(row["movieID"], row["name"], row["year"], row["minutes"],
                 make_category(row))


def get_categories():
    query = '''SELECT categoryID, name AS categoryName
               FROM Category'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    categories = []
    for row in results:
        categories.append(make_category(row))
    return categories


def get_category(category_id):
    query = '''SELECT categoryId, name AS categoryName
               FROM Category WHERE categoryID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (category_id,))
        row = c.fetchone()

    category = make_category(row)
    return category


def get_category_by_name(category_name):
    query = '''SELECT categoryId, name AS categoryName
               FROM Category WHERE categoryName = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (category_name,))
        row = c.fetchone()

    category = make_category(row)
    return category


def get_all_movies():
    query = '''SELECT movieID, Movie.name, year, minutes,
                      Movie.categoryId AS categoryID,
                      Category.name as categoryName
               FROM Movie JOIN Category ON Movie.categoryID = Category.categoryID
               ORDER BY Movie.name DESC'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    movies = []
    for row in results:
        movies.append(make_movie(row))
    return movies


def get_movies_by_category(category_id):
    query = '''SELECT movieID, Movie.name, year, minutes,
                      Movie.categoryId AS categoryID,
                      Category.name as categoryName
               FROM Movie JOIN Category ON Movie.categoryID = Category.categoryID
               WHERE Movie.categoryID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (category_id,))
        results = c.fetchall()

    movies = []
    for row in results:
        movies.append(make_movie(row))
    return movies


def get_movie(movie_id):
    query = '''SELECT movieID, Movie.name, year, minutes,
                      Movie.categoryId AS categoryID,
                      Category.name as categoryName
               FROM Movie JOIN Category ON Movie.categoryID = Category.categoryID
               WHERE movieID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (movie_id,))
        result = c.fetchone()
    return make_movie(result)


def get_movies_by_year(year):
    query = '''SELECT movieID, Movie.name, year, minutes,
                      Movie.categoryId AS categoryID,
                      Category.name as categoryName
               FROM Movie JOIN Category ON Movie.categoryID = Category.categoryID
               WHERE year = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (year,))
        results = c.fetchall()

    movies = []
    for row in results:
        movies.append(make_movie(row))
    return movies


def get_movies_by_minutes(mins):
    query = '''SELECT movieID, Movie.name, year, minutes,
                      Movie.categoryId AS categoryID,
                      Category.name as categoryName
               FROM Movie JOIN Category ON Movie.categoryID = Category.categoryID
               WHERE minutes < ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (mins,))
        results = c.fetchall()

    movies = []
    for row in results:
        movies.append(make_movie(row))
    return movies


def add_movie(movie):
    sql = '''INSERT INTO Movie (categoryID, name, year, minutes)
             VALUES (?, ?, ?, ?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (movie.category.id, movie.name, movie.year, movie.minutes))
        conn.commit()


def delete_movie(movie_id):
    sql = '''DELETE FROM Movie WHERE movieID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (movie_id,))
        conn.commit()
