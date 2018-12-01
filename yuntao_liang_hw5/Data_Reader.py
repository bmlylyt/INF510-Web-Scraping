
class DataReader:

    actor_list = None
    movie_list_by_default = None
    movie_list_by_rating = None

    def __init__(self):
        self.actor_list = list()
        self.movie_list_by_default = list()
        self.movie_list_by_rating = list()

    def get_actor_list(self):
        file = open('Actor.csv')
        header_line = file.readline()
        header = header_line.split(',')
        file_content = file.readlines()
        for i in range(len(file_content)):
            dct = dict()
            for j in range(len(header)):
                row = file_content[i].rstrip('\n')
                row_content = row.split(',')
                dct[header[j]] = row_content[j]
            self.actor_list.append(dct)
        return self.actor_list

    def get_movie_list_sorted_by_default(self):
        file = open('Movies_sorted_by_default.csv')
        self.read(file, self.movie_list_by_default)
        return self.movie_list_by_default

    def get_movie_list_sorted_by_rating(self):
        file = open('Movies_sorted_by_rating.csv')
        self.read(file, self.movie_list_by_rating)
        return self.movie_list_by_rating

    def read(self, file, lst):
        header_line = file.readline()
        header = header_line.split(',')
        file_content = file.readlines()
        for i in range(len(file_content)):
            dct = dict()
            for j in range(len(header)):
                row = file_content[i].rstrip('\n')
                row_content = row.split(',')
                dct[header[j]] = row_content[j]
            lst.append(dct)


