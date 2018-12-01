import urllib.request, urllib.parse, urllib.error
import json
import requests
from IPython.display import Image, display

class TmdbAPIGetter:

    web_url = 'https://api.themoviedb.org/3/'
    api_key = '4d228c24d92573df4456621bf2fd379c'
    genre = dict()

    def __init__(self):
        genre_url = 'https://api.themoviedb.org/3/genre/movie/list?api_key=4d228c24d92573df4456621bf2fd379c&language=en-US'
        data = requests.get(genre_url).content
        json_genre = json.loads(data)
        self.genre = json_genre

    '''sometimes the profile url in this result doesn't exist'''
    def search_movies_by_actor_name(self, name):
        name = name.split(' ')
        name = '%20'.join(name)
        original_url = 'https://api.themoviedb.org/3/search/person?api_key=4d228c24d92573df4456621bf2fd379c&language=en-US'
        actor_url = '&query={}&page=1&include_adult=false'.format(name)
        query_url = original_url + actor_url
        data = requests.get(query_url).content
        json_movie_by_actor = json.loads(data)
        return json_movie_by_actor['results']

    '''get profile here using profile_url'''
    def get_actor_by_id(self, id):
        actor_query = 'https://api.themoviedb.org/3/person/{}?api_key=4d228c24d92573df4456621bf2fd379c&language=en-US'.format(id)
        data = requests.get(actor_query).content
        actor_by_id = json.loads(data)
        return actor_by_id

    def get_profile_by_profile_url(self, url):
        profile_url = 'https://image.tmdb.org/t/p/w500' + url
        i = Image(profile_url, width=300, height=300)
        return i

    def get_genre_dict(self):
        return self.genre

# tmdb_getter = TmdbAPIGetter()
# print(tmdb_getter.get_movie_by_actor_name('Charlize Theron'))
# print(tmdb_getter.get_actor_by_id(6885))
# print(tmdb_getter.get_profile_by_profile_url('fG0mtmBm3OsvKFucvoQyqBnVwya.jpg'))
