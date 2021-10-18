from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from ..models import Car


# Create your tests here.
class CarViewSetTest(TestCase):
    """
    Test module for the /cars viewset
    """

    def test_view_url_exists(self) -> None:
        """
        Test whether the URL is accessible at the correct location
        """
        response = self.client.get("/cars/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_url_byname(self) -> None:
        """
        Test whether the URL is accessible by name (List View)
        """
        response = self.client.get(reverse("cars-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_car(self) -> None:
        """
        Test the POST request with valid data
        """
        sample_car = {"make": "Toyota", "model": "Supra"}
        response = self.client.post("/cars/", sample_car)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_car(self) -> None:
        """
        Test the POST request with invalid data
        """
        sample_car = {"make": "Fake", "model": "Car"}
        response = self.client.post("/cars/", sample_car)

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_delete_valid_car(self) -> None:
        """
        Test the DELETE request with valid data (id)
        """
        Car.objects.create(make="Toyota", model="Supra")
        response = self.client.delete("/cars/1/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_car(self) -> None:
        """
        Test the DELETE request with valid data (id)
        """
        Car.objects.create(make="Toyota", model="Supra")
        response = self.client.delete("/cars/2/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RateViewSetTest(TestCase):
    """
    Test module for the /cars viewset
    """

    def test_view_url_exists(self) -> None:
        """
        Test whether the URL is accessible at the correct location
        """
        response = self.client.get("/rate/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_url_byname(self) -> None:
        """
        Test whether the URL is accessible by name (List View)
        """
        response = self.client.get(reverse("rate-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_rating(self) -> None:
        """
        Test the POST request with valid ratings and valid car
        """
        # Create a car to post ratings to
        sample_car = {"make": "Toyota", "model": "Supra"}
        response = self.client.post("/cars/", sample_car)

        # Loop thorugh all the acceptable ratings
        for i in range(1, 6):
            sample_rating = {"car_id": 1, "rating": i}
            response = self.client.post("/rate/", sample_rating)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_rating(self) -> None:
        """
        Test the POST request with invalid ratings and valid car
        """
        # Create a car to post ratings to
        sample_car = {"make": "Toyota", "model": "Supra"}
        response = self.client.post("/cars/", sample_car)

        # Loop through some unacceptable ratings
        wrong_ratings = [-3, -1.3, 0, 0.5, 5.5, 8]
        for rating in wrong_ratings:
            sample_rating = {"car_id": 1, "rating": rating}
            response = self.client.post("/rate/", sample_rating)

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_rating_invalid_car(self) -> None:
        """
        Test the POST request with valid ratings and invalid car
        """
        # Loop thorugh all the acceptable ratings but with no car in DB
        for i in range(1, 6):
            sample_rating = {"car_id": 1, "rating": i}
            response = self.client.post("/rate/", sample_rating)

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_rating(self) -> None:
        """
        Test the DELETE request (should not be accessible)
        """
        response = self.client.delete("/rate/1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_average_rating(self) -> None:
        """
        Test the POST request: see if average rating is calculated properly
        """
        # Create a car to post ratings to
        sample_car = {"make": "Toyota", "model": "Supra"}
        self.client.post("/cars/", sample_car)

        # Verify it's rating is NULL upon creation
        car = Car.objects.get(id=1)
        self.assertEqual(car.avg_rating, None)

        # Add some ratings to the car
        ratings = [1, 1, 3, 5, 5, 4]  # Avg = 3.2
        for rating in ratings:
            sample_rating = {"car_id": 1, "rating": rating}
            self.client.post("/rate/", sample_rating)
        # Refresh the object instance
        car = Car.objects.get(id=1)
        self.assertEqual(car.avg_rating, 3.2)

    def test_average_votes(self) -> None:
        """
        Test the POST request: see if number of votes is calculated properly
        """
        # Create a car to post ratings to
        sample_car = {"make": "Toyota", "model": "Supra"}
        self.client.post("/cars/", sample_car)

        # Verify it's number of votes is 0 upon creation
        car = Car.objects.get(id=1)
        self.assertEqual(car.rates_number, 0)

        # Add some ratings to the car
        ratings = [1, 1, 3, 5, 5, 4]  # Votes = 6
        for rating in ratings:
            sample_rating = {"car_id": 1, "rating": rating}
            self.client.post("/rate/", sample_rating)
        # Refresh the object instance
        car = Car.objects.get(id=1)
        self.assertEqual(car.rates_number, 6)


class PopularViewSetTest(TestCase):
    """
    Test module for the /cars viewset
    """

    def test_view_url_exists(self) -> None:
        """
        Test whether the URL is accessible at the correct location
        """
        response = self.client.get("/popular/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_url_byname(self) -> None:
        """
        Test whether the URL is accessible by name (List View)
        """
        response = self.client.get(reverse("popular-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
