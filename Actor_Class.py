
class Actor:

    name = ''
    birthday = ''
    gender = ''
    profile = ''
    movies_attend = None

    def __init__(self, name, birthday, profile, gender):
        self.name = name
        self.birthday = birthday
        self.profile = profile
        self.gender = gender
        self.movies_attend = list()

    def add_movies(self, movie):
        self.movies_attend.append(movie)

    def get_name(self):
        return self.name

    def get_birthday(self):
        return self.birthday

    def get_gender(self):
        return self.gender

    def get_profile(self):
        return self.profile

    def get_movie_attend(self):
        return self.movies_attend

    def __str__(self):
        all_movies = ','.join(self.movies_attend)
        return 'name: {}, birthday: {}, gender: {}, profile: {} \nmovies_attend: {}'\
            .format(self.name, self.birthday, self.gender, self.profile, all_movies)