import json
import urllib.parse
import urllib.request
import os
def read_key():

    key = None

    try:
        with open('search.key','r') as f:
            key = f.readline().strip()
    except Exception as e:
        print(e.__cause__)

    return key

def replace(word):
    return word.replace(' ', '-')

def run_query(search_item, size=10):
    key = read_key()

    root_url = 'http://webhose.io/search'

    query_string = urllib.parse.quote(search_item)

    search_url = '{root_url}?token={key}&format=json&q={query}&sort=relevancy&size={size}'.format(
                          root_url=root_url,
                          key=key,
                          query=query_string,
                          size=size)

    results = []

    try:
        response = urllib.request.urlopen(search_url).read().decode('utf-8')

        json_response = json.loads(response)

        for post in json_response['posts']:
            results.append({
                'title': post['title'],
                'link': post['url'],
                'summary': post['text'][:200],
                'slug': replace(post['title'])
            })

    except Exception as e:
        print(e.__cause__)

    return results
