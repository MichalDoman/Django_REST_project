import pytest

from movielist.models import Movie
from showtimes.models import Cinema, Screening
from utils import create_test_cinema_data
from movielist.tests.utils import create_fake_movie


@pytest.mark.django_db
def test_add_cinema(client, set_up):
    cinemas_before = Cinema.objects.count()
    new_cinema = create_test_cinema_data()
    response = client.post("/cinemas/", new_cinema, format="json")
    assert response.status_code == 201
    assert Cinema.objects.count() == cinemas_before + 1
    for key, value in new_cinema.items():
        assert key in response.data
        assert response.data[key] == value


@pytest.mark.django_db
def test_get_cinema_list(client, set_up):
    response = client.get("/cinemas/", {}, format='json')

    assert response.status_code == 200
    assert Cinema.objects.count() == len(response.data)


@pytest.mark.django_db
def test_get_cinema_detail(client, set_up):
    cinema = Cinema.objects.first()
    response = client.get(f"/cinemas/{cinema.id}/", {}, format='json')

    assert response.status_code == 200
    for field in ("name", "city", "movies"):
        assert field in response.data


@pytest.mark.django_db
def test_delete_cinema(client, set_up):
    cinema = Cinema.objects.first()
    response = client.delete(f"/cinemas/{cinema.id}/", {}, format='json')
    assert response.status_code == 204
    cinema_ids = [cinema.id for cinema in Cinema.objects.all()]
    assert cinema.id not in cinema_ids


@pytest.mark.django_db
def test_update_cinema(client, set_up):
    cinema = Cinema.objects.first()
    response = client.get(f"/cinemas/{cinema.id}/", {}, format='json')
    cinema_data = response.data
    cinema_data["name"] = "updated_cinema_name"
    cinema_data["city"] = "updated_cinema_city"

    response = client.patch(f"/cinemas/{cinema.id}/", cinema_data, format='json')
    assert response.status_code == 200
    cinema_obj = Cinema.objects.get(id=cinema.id)
    assert cinema_obj.name == "updated_cinema_name"
    assert cinema_obj.city == "updated_cinema_city"


@pytest.mark.django_db
def test_add_screening(client, set_up):
    cinema = Cinema.objects.first()
    create_fake_movie()
    movie = Movie.objects.last()
    new_screening_data = {
        "movie": movie.title,
        "cinema": cinema.name,
        "date": "1410-07-15T00:00:00Z"
    }
    screening_count_before = Screening.objects.count()

    response = client.post("/screenings/", new_screening_data, format="json")
    assert response.status_code == 201
    assert Screening.objects.count() == screening_count_before + 1
    for key, value in new_screening_data.items():
        assert key in response.data
        assert response.data[key] == value


@pytest.mark.django_db
def test_get_screening_list(client, set_up):
    response = client.get("/screenings/", {}, format="json")

    assert response.status_code == 200
    assert Screening.objects.count() == len(response.data)


@pytest.mark.django_db
def test_get_screening_details(client, set_up):
    screening = Screening.objects.first()
    response = client.get(f'/screenings/{screening.pk}', {}, format="json")

    assert response.status_code == 200
    for field in ("movie", "cinema", "date"):
        assert field in response.data


@pytest.mark.django_db
def test_delete_screening(client, set_up):
    screening = Screening.objects.first()
    response = client.delete(f"/screenings/{screening.pk}", {}, format="json")
    assert response.status_code == 204
    screening_ids = [screening.id for screening in Screening.objects.all()]
    assert screening.id not in screening_ids


@pytest.mark.django_db
def test_update_screening(client, set_up):
    screening = Screening.objects.first()
    response = client.get(f"/screenings/{screening.pk}", {}, format="json")
    new_data = response.data
    new_data["date"] = "2000-07-15T00:00:00Z"

    response = client.patch(f"/screenings/{screening.pk}", new_data, format="json")
    assert response.status_code == 200
    screening_obj = Screening.objects.get(id=screening.id)
    assert screening_obj.date == "2000-07-15T00:00:00Z"
