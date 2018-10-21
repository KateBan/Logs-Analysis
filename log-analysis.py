#!/usr/bin/env python3
import psycopg2
from contextlib import contextmanager


@contextmanager
def create_cursor():
    """
    Helper function that creates cursor from a database connection by using the
    contextlib.
    """
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    yield c
    c.close()
    db.close()


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=news")


def mostPoppularArticles():
    """Returns the three articles that were accessed the most"""
    query = """
        SELECT title, num FROM articles,log_slug_views
        WHERE articles.slug = log_slug_views.slug
        ORDER BY num DESC LIMIT 3
        """
    with create_cursor() as c:
        c.execute(query)
        result = c.fetchall()
        for row in result:
            print(row[0], "Views: ", row[1])


def mostPopularArticleAuthors():
    """Returns which authors get the most page views"""
    query = """
        SELECT name, SUM(num) as result
        FROM ready_to_sum_author_articles
        GROUP BY name
        ORDER BY result DESC
        """

    with create_cursor() as c:
        c.execute(query)
        results = c.fetchall()
        for row in (results):
            print(row[0], "Views: ", row[1])


def statusErrors():
    """Returns On which days did more than 1% of requests lead to errors"""
    query = """
        SELECT * FROM percents WHERE perc > 1.0
        """
    with create_cursor() as c:
        c.execute(query)
        result = c.fetchall()
        for row in result:
            print("On", row[0], "there were", round(row[1], 2), "% errors.")


print("*" * 22, 'REPORT', "*" * 22)
print()
print("The most the most popular three articles of all time")
print("*" * 53)
mostPoppularArticles()
print()

print("The most popular article authors of all time")
print("*" * 53)
mostPopularArticleAuthors()
print()

print("Days on which more than 1% of requests lead to errors")
print("*" * 53)
statusErrors()
print()
