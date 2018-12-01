import urllib.request, urllib.parse, urllib.error
import json

class OmdbAPIGetter:

    web_url = ''
    api_key = ''

    def __init__(self):
        self.web_url = 'http://www.omdbapi.com/?'
        self.api_key = '&apikey=ada1059e'

    def get_by_title(self, title):
        name_list = title.split(' ')
        full_name = '+'.join(name_list)
        query = 't={}'.format(full_name)
        url_query = self.web_url + query + self.api_key
        try:
            response = urllib.request.urlopen(url_query)
            data = response.read().decode()
        except:
            print('Wrong Request')
            return
        json_response = json.loads(data)
        return json_response

    def search_by_title(self, title):
        name_list = title.split(' ')
        full_name = '+'.join(name_list)
        query = 's={}'.format(full_name)
        url_query = self.web_url + query + self.api_key
        try:
            response = urllib.request.urlopen(url_query)
            data = response.read().decode()
        except:
            print('Wrong Request')
            return
        json_response = json.loads(data)
        return json_response['Search']


# json_getter = OmdbAPIGetter()
# json_get = json_getter.get_by_title('Star Wars')
# json_search = json_getter.search_by_title('Star Wars')
# print(json_get)
# for i in json_search:
#     print(i)