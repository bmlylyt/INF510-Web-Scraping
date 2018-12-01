import time
import functools
import sys
from sys import argv

from OMDB_API_Getter import OmdbAPIGetter
from TMDB_API_Getter import TmdbAPIGetter
from RT_Scraper import RTScraper
from Actor_Class import Actor
from Movie_Class import Movie
from Data_Reader import DataReader


# self defined comparator, sorting list by rating property
def comparator(a, b):
    rating1 = a[3]
    rating2 = b[3]
    if rating1 != 'N/A' and rating2 != 'N/A':
        if '/' in rating1:
            loc = rating1.find('/')
            rating1 = int(rating1[0:loc])
        else:
            rating1 = int(rating1[0:len(rating1) - 1])

        if '/' in rating2:
            loc = rating2.find('/')
            rating2 = int(rating2[0:loc])
        else:
            rating2 = int(rating2[0:len(rating2) - 1])

        if rating1 < rating2:
            return -1
        elif rating1 > rating2:
            return 1
        else:
            return 0
    elif rating1 != 'N/A' and rating2 == 'N/A':
        return 1
    elif rating1 == 'N/A' and rating2 != 'N/A':
        return -1
    else:
        return 0

''' 
    Get more detail information using web API of OMDB, including actors, year, ratings, 
    box office and poster
'''


def get_detail(Omdb_getter, top_100_best_movies_list):
    movie_detail_list = list()
    for movie in top_100_best_movies_list:
        movie_detail_dict = dict()
        movie_name = movie['movie_name']
        movie_detail = Omdb_getter.get_by_title(movie_name)
        try:
            movie_detail_dict['Title'] = movie_detail['Title']
        except:
            movie_detail_dict['Title'] = movie_name
        try:
            movie_detail_dict['Actors'] = movie_detail['Actors']
        except:
            movie_detail_dict['Actors'] = 'Data not exist'
        try:
            movie_detail_dict['Genre'] = movie_detail['Genre']
        except:
            movie_detail_dict['Genre'] = 'Data not exist'
        try:
            movie_detail_dict['Year'] = movie_detail['Year']
        except:
            movie_detail_dict['Year'] = 'Data not exist'
        try:
            movie_detail_dict['Ratings'] = movie_detail['Ratings']
        except:
            movie_detail_dict['Ratings'] = 'Data not exist'
        try:
            movie_detail_dict['BoxOffice'] = movie_detail['BoxOffice']
        except:
            movie_detail_dict['BoxOffice'] = 'Data not exist'
        try:
            movie_detail_dict['Poster'] = movie_detail['Poster']
        except:
            movie_detail_dict['Poster'] = 'Data not exist'
        try:
            movie_detail_dict['Awards'] = movie_detail['Awards']
        except:
            movie_detail_dict['Awards'] = 'Data not exist'

        movie_detail_list.append(movie_detail_dict)
        time.sleep(0.03)

    return movie_detail_list

'''
    Get actor dictionary that store the actor object who play a main role in that movie
    by using the movie list we get above and another web API, TMDB_API
'''


def get_actor(top100_best_movie_detail_list, Tmdb_getter):
    actor_dict = dict()
    for movie in top100_best_movie_detail_list:
        actors = movie['Actors'].split(', ')
        for actor_name in actors:

            # the results includes the actor id and all the movies this actor played
            movie_to_get_id = Tmdb_getter.search_movies_by_actor_name(actor_name)

            # get the actor id who play a role in this movie
            try:
                actor_id = movie_to_get_id[0]['id']
            except:
                continue
            # use TMDB API to get the actor information
            actor_info = Tmdb_getter.get_actor_by_id(actor_id)
            name = actor_info['name']
            birthday = actor_info['birthday']
            profile = actor_info['profile_path']
            gender = ''
            if actor_info['gender'] == 1:
                gender = 'female'
            else:
                gender = 'male'

            # create the actor object
            new_actor = Actor(name, birthday, profile, gender)

            actor_dict[name] = new_actor

            # append all the movies this actor played to the movie list of the actor object
            append_movies_to_actor(actor_dict[name], movie_to_get_id)

        time.sleep(0.03)
    return actor_dict


'''
    fill out the movies attended field in Actor class
'''


def append_movies_to_actor(new_actor, movies_attended):
    for dic in movies_attended:
        if dic['name'] == new_actor.get_name():
            for movie in dic['known_for']:

                # only care about movies, tv is not included
                if movie['media_type'] == 'movie':
                    new_actor.add_movies(movie['title'])
    print(new_actor)


'''
    use the data information we get above to instantiate the movie object
    and store this object to move list
'''


def get_movie(top_movies_actors_dic, top100_best_movie_detail_list):

    movie_list = list()
    for movie_detail in top100_best_movie_detail_list:
        # extract the field
        Title = movie_detail['Title']
        Genre = movie_detail['Genre']
        Year = movie_detail['Year']
        Ratings = movie_detail['Ratings']
        BoxOffice = movie_detail['BoxOffice']
        Poster = movie_detail['Poster']
        Awards = movie_detail['Awards']

        # create the movie object
        new_movie = Movie(Title, Genre, Year, Ratings, BoxOffice, Poster, Awards)

        # add actors object to actor list in movie field
        actor_names = movie_detail['Actors']
        append_actors_to_movie(new_movie, top_movies_actors_dic, actor_names)
        movie_list.append(new_movie)
    print(len(movie_list))
    return movie_list


'''
    add the actor objects we created above to the actors field of movie objects
'''


def append_actors_to_movie(new_movie, top_movies_actors_dic, actor_names):
    for actor_name in actor_names.split(', '):
        if actor_name in top_movies_actors_dic:
            new_movie.add_actor(top_movies_actors_dic[actor_name])


'''
    Store the actor objects we create who attended in top 100 movies to CSV file
'''


def store_actors_to_csv(top_movies_actors_dic):
    actor_file = open('Actor.csv', 'w')
    header_line = 'name,birthday,profile,gender,movie_attended'
    actor_file.write(header_line)
    actor_file.write('\n')
    for actor_name in top_movies_actors_dic:
        lst = list()
        cur_actor = top_movies_actors_dic[actor_name]
        lst.append(cur_actor.get_name())
        lst.append(cur_actor.get_birthday())
        lst.append(cur_actor.get_profile())
        lst.append(cur_actor.get_gender())
        lst.append('. '.join(cur_actor.get_movie_attend()))
        str = ''
        for i in lst:
            if i is None:
                i = ' '
            str += i + ','
        actor_file.write(str[0:len(str) - 1])
        actor_file.write('\n')


'''
    Store the top 100 movies to csv file
'''


def store_movies_to_csv(top100_movies_list):
    sorted_by_top = list()
    movie_file = open('Movies_sorted_by_default.csv', 'w')
    header_line = 'Title, Genre, Year, Ratings, BoxOffice, Poster, Awards, Actors'
    movie_file.write(header_line)
    movie_file.write('\n')
    for movie in top100_movies_list:
        lst = list()
        title = movie.get_title()
        if ',' in title:
            title = '，'.join(title.split(','))
        lst.append(title)
        lst.append('/'.join(movie.get_genre().split(', ')))
        lst.append(movie.get_year())
        ratings = movie.get_rating()
        rating = 'N/A'
        if ratings != 'Data not exist':
            try:
                rating = ratings[1].get('Value')
            except:
                rating = 'N/A'
        lst.append(rating)
        lst.append(' '.join(movie.get_box_office().split(',')))
        lst.append(movie.get_poster())
        awards = movie.get_awards().split(',')
        awards = '. '.join(awards)
        lst.append(awards)
        actors = ''
        for actor in movie.get_actor():
            actors += actor.get_name() + '. '
        lst.append(actors[0: len(actors) - 2])
        str = ''
        sorted_by_top.append(lst)
        for i in lst:
            if i is None:
                i = ' '
            if i == 'Data not exist':
                i = 'N/A'
            str += i + ','
        movie_file.write(str[0:len(str) - 1])
        movie_file.write('\n')
    return sorted_by_top


'''
    re-order the movie list by rating from rotten tomatoes
'''


def store_movies_to_csv_by_rating(sorted_by_default):
    sorted_by_rating = sorted(sorted_by_default, key=functools.cmp_to_key(comparator), reverse=True)
    movie_file = open('Movies_sorted_by_rating.csv', 'w')
    header_line = 'Title, Genre, Year, Ratings, BoxOffice, Poster, Awards, Actors'
    movie_file.write(header_line)
    movie_file.write('\n')
    for movies in sorted_by_rating:
        str = ','.join(movies)
        movie_file.write(str)
        movie_file.write('\n')
    return sorted_by_rating


# Final movie list we are going to store to disk
# Final top movie actors list we are going to store to disk
top100_best_movie_detail_list = dict()
top100_movies_list = list()
top100_movies_actors_dic = dict()


# read data from remote
def read_data_from_remote():
    # initial the getter object
    Omdb_getter = OmdbAPIGetter()
    Tmdb_getter = TmdbAPIGetter()
    rt_scraper = RTScraper()

    # Sorted by priority list
    sorted_by_default = list()
    sorted_by_rating = list()

    # Get the title of top100 best movie using web scraper
    top100_best_movies_title_list = rt_scraper.top100_best_movies()

    # Get more detail information using web API of OMDB, including actors, year, ratings, box office and poster
    top100_best_movie_detail_list = get_detail(Omdb_getter, top100_best_movies_title_list)

    # Get actor dictionary that store the actor who play a main role in that movie
    # by using the movie list we get above and another web API, TMDB_API
    top100_movies_actors_dic = get_actor(top100_best_movie_detail_list, Tmdb_getter)

    # Wrap all the information related to the movie into object and store in top100_movie_list
    top100_movies_list = get_movie(top100_movies_actors_dic, top100_best_movie_detail_list)

    # Store the actors who appeared in top movies to csv file
    store_actors_to_csv(top100_movies_actors_dic)

    # Store the top 100 movies to csv file
    sorted_by_default = store_movies_to_csv(top100_movies_list)
    sorted_by_rating = store_movies_to_csv_by_rating(sorted_by_default)


''' main method '''

if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == '--source=remote':
        # Read data from remote
        read_data_from_remote()

    elif sys.argv[1] == '--source=local':
        try:
            # Initial the data reader
            data_reader = DataReader()
            # Get the actors data from disk
            actor_list = data_reader.get_actor_list()
            # Get the movies sorted by default from disk
            movie_list_sorted_by_default = data_reader.get_movie_list_sorted_by_default()
            # Get the movies sorted by rating from disk
            movie_list_sorted_by_rating = data_reader.get_movie_list_sorted_by_rating()

            for i in movie_list_sorted_by_rating:
                print(i)

        except:
            print('The file you want to open is not exist, please read them from remote first')
    else:
        print('Wrong parameter')

