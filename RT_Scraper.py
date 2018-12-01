from bs4 import BeautifulSoup
import requests

'''
    Scraper class has three method to get the three type
    of top 100 movies, the best 100 movies all the time, the 
    best 100 animation movies and the best 100 fiction movies
'''
class RTScraper:

    rt_url = 'https://www.rottentomatoes.com/top/'
    soup = None
    main_table = None;

    def __init__(self):
        page = requests.get(self.rt_url)
        self.soup = BeautifulSoup(page.content, 'html.parser')
        rt_url = 'https://www.rottentomatoes.com/top/'
        page = requests.get(rt_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        self.main_table = soup.find('div', {'class': 'container-masonry'})

    def top100_animation_movies(self):

        anim_list = list()
        top_table = self.main_table.find_all('div', {'class': 'item'})[2]
        top_list = top_table.find('ul', {'class': 'genrelist'}).find_all('li')
        top_animation_url = 'https://www.rottentomatoes.com' + top_list[1].a['href']
        animation_page = requests.get(top_animation_url)
        animation_soup = BeautifulSoup(animation_page.content, 'html.parser')
        animation_table = animation_soup.find('table', {'class': 'table'})
        animation_list = animation_table.find_all('tr')
        for animation in animation_list[1:]:
            anim_dict = dict()
            name_year = animation.a.text
            rating = animation.find('span', {'class': 'tMeterScore'}).text
            left = 13
            right = name_year.rfind(' ')
            anim_dict['movie_name'] = name_year[left:right]
            anim_dict['release_year'] = name_year[right + 2: len(name_year) - 1]
            anim_dict['rt_rating'] = rating[1:]
            anim_list.append(anim_dict)
        return anim_list

    def top100_best_movies(self):

        top_table = self.main_table.find_all('div', {'class': 'item'})[3]
        top_url = 'https://www.rottentomatoes.com' + top_table.find('div', {'class': 'fr'}).a['href']
        top_page = requests.get(top_url)
        top_soup = BeautifulSoup(top_page.content, 'html.parser')
        top_table = top_soup.find('table', {'class': 'table'})
        top_list = top_table.find_all('tr')
        top_movie_list = list()
        for top in top_list[1:]:
            top_dict = dict()
            name_year = top.a.text
            rating = top.find('span', {'class': 'tMeterScore'}).text
            left = 13
            right = name_year.rfind(' ')
            top_dict['movie_name'] = name_year[left:right]
            top_dict['release_year'] = name_year[right + 2: len(name_year) - 1]
            top_dict['rt_rating'] = rating[1:]
            top_movie_list.append(top_dict)
        return top_movie_list

    def top100_fiction_movies(self):
        fiction_movie_list = list()
        fiction_table = self.main_table.find_all('div', {'class': 'item'})[2]
        fiction_list = fiction_table.find('ul', {'class': 'genrelist'}).find_all('li')
        top_fiction_url = 'https://www.rottentomatoes.com' + fiction_list[12].a['href']
        fiction_page = requests.get(top_fiction_url)
        fiction_soup = BeautifulSoup(fiction_page.content, 'html.parser')
        fiction_table = fiction_soup.find('table', {'class': 'table'})
        fiction_list = fiction_table.find_all('tr')
        for fiction in fiction_list[1:]:
            fiction_dict = dict()
            name_year = fiction.a.text
            rating = fiction.find('span', {'class': 'tMeterScore'}).text
            left = 13
            right = name_year.rfind(' ')
            fiction_dict['movie_name'] = name_year[left:right]
            fiction_dict['release_year'] = name_year[right + 2: len(name_year) - 1]
            fiction_dict['rt_rating'] = rating[1:]
            fiction_movie_list.append(fiction_dict)
        return fiction_movie_list


# RT_url = 'https://www.rottentomatoes.com/top/'
# page = requests.get(RT_url)
# soup = BeautifulSoup(page.content, 'html.parser')
# main_table = soup.find('div', {'class':'container-masonry'})


'''Scrper the top animation'''
# top_table = main_table.find_all('div',{'class':'item'})[2]
# top_list = top_table.find('ul', {'class':'genrelist'})
# top_list = top_list.find_all('li')

# top_animation_url = 'https://www.rottentomatoes.com' + top_list[1].a['href']
# animation_page = requests.get(top_animation_url)
# animation_soup = BeautifulSoup(animation_page.content, 'html.parser')
# animation_table = animation_soup.find('table', {'class':'table'})
# animation_list = animation_table.find_all('tr')
#
# for animation in animation_list[1:]:
#     anim_dict = dict()
#     name_year = animation.a.text
#     left = 13
#     right = name_year.rfind(' ')
#     print(name_year[left:right + 1])
#     print(name_year[right+2: len(name_year) - 1])

'''Scrape the top 100 movie all the time'''
# top_table = main_table.find_all('div',{'class':'item'})[3]
# top_url = 'https://www.rottentomatoes.com' + top_table.find('div',{'class':'fr'}).a['href']
# print(top_url)
# top_page = requests.get(top_url)
# top_soup = BeautifulSoup(top_page.content, 'html.parser')
# top_table = top_soup.find('table', {'class': 'table'})
# top_list = top_table.find_all('tr')
# top_movie_list = list()
# for top in top_list[1:]:
#     top_dict = dict()
#     name_year = top.a.text
#     rating = top.find('span',{'class':'tMeterScore'}).text
#     left = 13
#     right = name_year.rfind(' ')
#     top_dict['movie_name'] = name_year[left:right]
#     top_dict['release_year'] = name_year[right + 2: len(name_year) - 1]
#     top_dict['rt_rating'] = rating
#     top_movie_list.append(top_dict)
# print(len(top_movie_list))

# rt_scraper = RTScraper()
# anim_list = rt_scraper.top100_animation_movies()
# top_list = rt_scraper.top100_best_movies()
# fiction_list = rt_scraper.top100_fiction_movies()
# for each in fiction_list:
#     print(each)

