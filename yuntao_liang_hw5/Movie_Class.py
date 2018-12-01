
class Movie:

    Title = ''
    Genre = ''
    Year = ''
    Ratings = ''
    BoxOffice = ''
    Poster = ''
    Awards = ''
    Actors = None

    def __init__(self, Title, Genre, Year, Ratings, BoxOffice, Poster, Awards):
        self.Title = Title
        self.Genre = Genre
        self.Year = Year
        self.Ratings = Ratings
        self.BoxOffice = BoxOffice
        self.Poster = Poster
        self.Awards = Awards
        self.Actors = list()

    def add_actor(self, actor):
        self.Actors.append(actor)

    def get_actor(self):
        return self.Actors

    def get_title(self):
        return self.Title

    def get_genre(self):
        return self.Genre

    def get_rating(self):
        return self.Ratings

    def get_box_office(self):
        return self.BoxOffice

    def get_year(self):
        return self.Year

    def get_poster(self):
        return self.Poster

    def get_awards(self):
        return self.Awards

    def __str__(self):
        str_info = 'Title: {}, Genre: {}, Year: {}, Rating: {}, BoxOffice: {}, Awards: {}'\
        .format(self.Title, self.Genre, self.Year, self.Ratings, self.BoxOffice, self.Awards)
        str_actors = '\n'
        for actor in self.Actors:
            str_actors += actor.__str__() + '\n'
        return str_info + str_actors