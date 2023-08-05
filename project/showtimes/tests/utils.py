from movielist.models import Movie
from showtimes.models import Cinema, Screening
from faker import Faker
from random import sample

faker = Faker("pl-PL")


def create_test_cinema():
    cinema = Cinema.objects.create(**create_test_cinema_data())
    create_test_screenings(cinema)


def create_test_cinema_data():
    cinema = {
        "name": faker.name(),
        "city": faker.city(),
    }
    return cinema


def create_test_screenings(cinema):
    movies = sample(list(Movie.objects.all()), 3)

    for movie in movies:
        Screening.objects.create(
            movie=movie,
            cinema=cinema,
            date="1410-07-15"  # Użyj datetime
        )
