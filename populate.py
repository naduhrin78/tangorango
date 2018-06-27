import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TangoRango.settings')

import django

django.setup()

from rango.models import Category, Page

def populate():
    python_pages = [
            {"title": "Official Python Tutorial",
            "url": "http://docs.python.org/2/tutorial/"},

            {"title": "How to Think like a Computer Scientist",
            "url": "http://www.greenteapress.com/thinkpython/"},

            {"title": "Learn Python in 10 Minutes",
            "url": "http://www.korokithakis.net/tutorials/python/"}
        ]

    django_pages = [
            {"title": "Official Django Tutorial",
             "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},

            {"title": "Django Rocks",
             "url": "http://www.djangorocks.com/"},

            {"title": "How to Tango with Django",
             "url": "http://www.tangowithdjango.com/"}

        ]

    other_pages = [
        {"title": "Bottle",
        "url":"http://bottlepy.org/docs/dev/"},

        {"title": "Flask",
        "url": "http://flask.pocoo.org"}

        ]

    cats = {
        "Python": {"pages": python_pages},
        "Django": {"pages": django_pages},
        "Other": {"pages": other_pages},
    }

    for cat, cat_items in cats:
        c = add_cat(cat)
        for cat_item in cat_items["pages"]:
            add_page(title=cat_item["title"], url=cat_item["url"], category=c)


def add_page(title, url, category):
    p = Page(category = category, views = 0, url = url, title = title)
    p.save()
    return p

def add_cat(name):
    c = Category(name = name)
    c.save()
    return c

if __name__ == '__main__':
    print("Starting population...")
    populate()


