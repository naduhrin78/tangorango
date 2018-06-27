import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TangoRango.settings')

import django

django.setup()

from rango.models import Category, Page

def populate():
    python_pages = [
            {"title": "Official Python Tutorial",
            "url": "http://docs.python.org/2/tutorial/",
            "views":100,
             },

            {"title": "How to Think like a Computer Scientist",
            "url": "http://www.greenteapress.com/thinkpython/",
            "views":50
             },

            {"title": "Learn Python in 10 Minutes",
            "url": "http://www.korokithakis.net/tutorials/python/",
            "views":25
            }
        ]

    django_pages = [
            {"title": "Official Django Tutorial",
             "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
             "views":90
             },

            {"title": "Django Rocks",
             "url": "http://www.djangorocks.com/",
             "views":60
            },

            {"title": "How to Tango with Django",
             "url": "http://www.tangowithdjango.com/",
             "views":30
            }

        ]

    other_pages = [
        {"title": "Bottle",
        "url":"http://bottlepy.org/docs/dev/",
        "views":80
        },

        {"title": "Flask",
        "url": "http://flask.pocoo.org",
        "views":40
        }

        ]

    cats = {
        "Python": {"pages": python_pages, "views": 128, "likes": 64},
        "Django": {"pages": django_pages, "views": 64, "likes": 32},
        "Other": {"pages": other_pages, "views": 32, "likes": 16},
    }

    for cat, cat_items in cats.items():
        c = add_cat(name=cat, views=cat_items["views"], likes=cat_items["likes"])
        for cat_item in cat_items["pages"]:
            add_page(title=cat_item["title"], url=cat_item["url"], category=c,views=cat_item["views"])


def add_page(title, url, category, views = 0):
    p, created = Page.objects.get_or_create(category=category, views=views, url=url, title=title)
    p.save()
    return p

def add_cat(name, views = 0, likes = 0):
    c, created = Category.objects.get_or_create(name=name, views=views, likes=likes)
    c.save()
    return c

if __name__ == '__main__':
    print("Starting population...")
    populate()


