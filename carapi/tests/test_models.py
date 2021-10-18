from django.test import TestCase
from ..models import *


# Create your tests here.
class CarTest(TestCase):
    """
    Test module for the Car model
    """

    def setUp(self) -> None:
        Car.objects.create(make="Toyota", model="Supra")
        Car.objects.create(make="Volkswagen", model="Golf")
        Car.objects.create(make="Fake", model="Car")

    def test_fields(self) -> None:
        """
        Test whether the attributes are created with desired parameters
        """
        car = Car.objects.get(id=1)
        make_length = car._meta.get_field("make").max_length
        model_length = car._meta.get_field("model").max_length

        self.assertEqual(make_length, 50)
        self.assertEqual(model_length, 50)

    def test_car_str(self) -> None:
        """
        Test whether the model is properly represented as a string
        """
        car_1 = Car.objects.get(id=1)
        car_2 = Car.objects.get(id=2)

        self.assertEqual(str(car_1), "Toyota Supra")
        self.assertEqual(str(car_2), "Volkswagen Golf")

    def test_car_make(self) -> None:
        """
        Test whether the correct make names have been assigned to DB objects
        """
        car_1 = Car.objects.get(id=1)
        car_2 = Car.objects.get(id=2)

        self.assertEqual(car_1.make, "Toyota")
        self.assertEqual(car_2.make, "Volkswagen")

    def test_car_model(self) -> None:
        """
        Test whether the correct model names have been assigned to DB objects
        """
        car_1 = Car.objects.get(id=1)
        car_2 = Car.objects.get(id=2)

        self.assertEqual(car_1.model, "Supra")
        self.assertEqual(car_2.model, "Golf")

    def test_car_avg_rating(self) -> None:
        """
        Test whether the correct avg_rating is assigned to DB objects
        """
        car_1 = Car.objects.get(id=1)
        car_2 = Car.objects.get(id=2)

        car_1.rate(1)
        car_1.rate(1)
        car_1.rate(5)  # Average = 1+1+5/3 = 2.(3)

        car_2.rate(1)
        car_2.rate(5)  # Average = 1+5/2 = 3.0

        self.assertEqual(car_1.avg_rating, 2.3)
        self.assertEqual(car_2.avg_rating, 3.0)

    def test_car_rates_number(self) -> None:
        """
        Test whether the correct rates_number is assigned to DB objects
        """
        car_1 = Car.objects.get(id=1)
        car_2 = Car.objects.get(id=2)

        car_1.rate(1)
        car_1.rate(1)
        car_1.rate(5)  # Votes = 3

        car_2.rate(1)
        car_2.rate(5)  # Votes = 2

        self.assertEqual(car_1.rates_number, 3)
        self.assertEqual(car_2.rates_number, 2)

    def test_car_external_api(self) -> None:
        """
        Test external API check
        """
        self.assertTrue(Car.checkNHTSAApi("Toyota", "Supra"))
        self.assertFalse(Car.checkNHTSAApi("Fake", "Car"))


class RatingTest(TestCase):
    """
    Test module for the Ratings model
    """

    def setUp(self) -> None:
        Car.objects.create(make="Toyota", model="Supra")
        Car.objects.create(make="Volkswagen", model="Golf")
        Car.objects.create(make="Fake", model="Car")

        car_1 = Car.objects.get(id=1)
        car_2 = Car.objects.get(id=2)
        car_3 = Car.objects.get(id=3)

        Rating.objects.create(car_id=car_1, rating=1)
        Rating.objects.create(car_id=car_1, rating=5)
        Rating.objects.create(car_id=car_1, rating=5)  # Average 3,7, votes 3

        Rating.objects.create(car_id=car_2, rating=5)
        Rating.objects.create(car_id=car_2, rating=1)
        Rating.objects.create(car_id=car_2, rating=3)  # Average 3.0, votes 3

        Rating.objects.create(car_id=car_3, rating=2)
        Rating.objects.create(car_id=car_3, rating=1)  # Average 1.5, votes 2

    def test_rating_exists(self) -> None:
        """
        Test whether Rating objects are properly created in the DB
        """
        rating1_1 = list(Rating.objects.filter(car_id=1))[0].rating
        rating1_2 = list(Rating.objects.filter(car_id=1))[1].rating
        rating1_3 = list(Rating.objects.filter(car_id=1))[2].rating

        rating2_1 = list(Rating.objects.filter(car_id=2))[0].rating
        rating2_2 = list(Rating.objects.filter(car_id=2))[1].rating
        rating2_3 = list(Rating.objects.filter(car_id=2))[2].rating

        rating3_1 = list(Rating.objects.filter(car_id=3))[0].rating
        rating3_2 = list(Rating.objects.filter(car_id=3))[1].rating

        self.assertEqual(rating1_1, 1)
        self.assertEqual(rating1_2, 5)
        self.assertEqual(rating1_3, 5)

        self.assertEqual(rating2_1, 5)
        self.assertEqual(rating2_2, 1)
        self.assertEqual(rating2_3, 3)

        self.assertEqual(rating3_1, 2)
        self.assertEqual(rating3_2, 1)

    def test_rating_car(self) -> None:
        """
        Test whether Rating objects are properly assigned to Cars
        """
        rated_car1_1 = str(list(Rating.objects.filter(car_id=1))[0].car_id)
        rated_car1_2 = str(list(Rating.objects.filter(car_id=1))[1].car_id)
        rated_car1_3 = str(list(Rating.objects.filter(car_id=1))[2].car_id)

        rated_car2_1 = str(list(Rating.objects.filter(car_id=2))[0].car_id)
        rated_car2_2 = str(list(Rating.objects.filter(car_id=2))[1].car_id)
        rated_car2_3 = str(list(Rating.objects.filter(car_id=2))[2].car_id)

        rated_car3_1 = str(list(Rating.objects.filter(car_id=3))[0].car_id)
        rated_car3_2 = str(list(Rating.objects.filter(car_id=3))[1].car_id)

        self.assertEqual(rated_car1_1, "Toyota Supra")
        self.assertEqual(rated_car1_2, "Toyota Supra")
        self.assertEqual(rated_car1_3, "Toyota Supra")

        self.assertEqual(rated_car2_1, "Volkswagen Golf")
        self.assertEqual(rated_car2_2, "Volkswagen Golf")
        self.assertEqual(rated_car2_3, "Volkswagen Golf")

        self.assertEqual(rated_car3_1, "Fake Car")
        self.assertEqual(rated_car3_2, "Fake Car")
