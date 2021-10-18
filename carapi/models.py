from django.db import models
from django.db.models.deletion import CASCADE
from django.core.validators import MinValueValidator, MaxValueValidator
import requests


# Create your models here.
class Car(models.Model):
    """
    Car class that allowes us to create objects in the database

    Attributes:
        id (int):           A unique id primary key is created by Django
        make (str):         Name of the make of the car, max 50 chars
        model (str):        Name of the model of the car, max 50 chars.
                            Make & Model combination should be unique.
        avg_rating (float): Average rating for the car, defaults to NULL
                            when no ratings have been posted for given car.
                            Not required when creating an instance.
        rates_number (int): Number of ratings for a given car, defaults to 0
                            when no ratings have been posted for given car.
                            Not required when creating an instance.
    """

    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    avg_rating = models.FloatField(blank=True, null=True)
    rates_number = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        unique_together = ("make", "model")

    def __str__(self) -> str:
        """
        Represent car object as "Make Model"
        """
        return self.make + " " + self.model

    @classmethod
    def check_nhtsa_api(cls, make, model) -> bool:
        """
        Contacts the external NHTSA Vehicle API, to verify whether
        the provided make & model combination is valid.

        Attributes:
            url (str):         The address of the external API method
            make (str):        The make of the car, as per request
            model (str):       The model of the car, as per request

        """
        url = (
            "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/"
            + make
            + "?format=json"
        )
        # Make request to external API, 5s timeout
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            results = r.json()["Results"]
            # Check for model name in the manufacturer's list of models
            for item in results:
                if model.lower() == item["Model_Name"].lower():
                    return True
            return False
        else:
            # Unable to contact API (no HTTP_200_SUCCESS code)
            return False

    def rate(self, new_rating) -> None:
        """
        Calculates the new rating
        Function is called whenever there is a successful POST /rate/ request.
        See views.RateViewSet.create() for details

        Keyword arguments:
            new_rating (float): New rating to be added, specified
                                in the POST /rate/ request.
        """
        # The following variables are added for code readability
        # Old rating, default 0, when none exists yet
        old = float(0.0 if self.avg_rating is None else self.avg_rating)
        # New rating, specified in the POST /rate/ request
        new = float(new_rating)
        # Number of current ratings, default 0, when none exists yet
        votes = int(0 if self.rates_number is None else self.rates_number)

        # Calculate the new average rating and round to 1 decimal point
        self.avg_rating = round(((old * votes) + new) / (votes + 1), 1)
        # Increase the number of votes
        # Important - this has to happen after average rating calculation!
        self.rates_number = votes + 1
        # Save the changes to the object
        self.save(update_fields=["avg_rating", "rates_number"])
        # return None


class Rating(models.Model):
    """
    Rating class that allowes us to create ratings associated with cars
    exisiting in the database.

    Attributes:
        car_id (int):       Foreign key associated with the ID of a vehicle
                            in the Car class.
                            If the car is deleted, delete all the ratings.
        rating (int):       Value between 1 to 5 to be added as a rating for
                            the given car. Used to calculate average rating.
    """

    car_id = models.ForeignKey(Car, on_delete=CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
