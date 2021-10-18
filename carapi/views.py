from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from .serializers import (
    CarSerializer,
    CarSerializerGet,
    CarSerializerPost,
    CarSerializerDelete,
    RatingSerializer,
    PopularSerializer,
)
from .models import Car, Rating


# Create your views here
class CarViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint that shows all the cars in the database.
    Allows listing: GET /cars/
    Allows posting: POST /cars/{make:str, model:str}/
    Allows deletion: DELETE /cars/{id:int}

    Attributes:
        queryset:          Looks through all the Car objects in the DB
        serializer_class:  Provides a default serializer for the class
        action_serializer: Picks the correct  serializer based on request
    """

    queryset = Car.objects.all()
    serializer_class = CarSerializer
    action_serializers: dict = {
        "list": CarSerializerGet,
        "create": CarSerializerPost,
        "destroy": CarSerializerDelete,
    }

    def get_serializer_class(self):
        """
        Override the class method to allow us to pick the correct serializer
        based on the request. Defaults to CarSerializer (all fields)
        """
        if hasattr(self, "action_serializers"):
            return self.action_serializers.get(
                self.action, self.serializer_class
            )

        return super(CarViewSet, self).get_serializer_class()

    def create(self, request, *args, **kwargs):
        """
        Override the POST method to allow us to verify whether the car
        exists in the external API database, before adding it.
        Using https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check external API for existence of the car
            if Car.check_nhtsa_api(
                request.data["make"], request.data["model"]
            ):
                # Save the car info
                serializer.save()
                return Response(
                    {"status": "success", "data": serializer.data},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {
                        "status": "error",
                        "data": (
                            request.data["make"]
                            + " "
                            + request.data["model"]
                            + " doesn't exist"
                        ),
                    },
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
        else:
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_404_NOT_FOUND,
            )


class RateViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    API endpoint that shows Ratings for given Cars in the database
    Allows listing: GET /rate/ - not needed per specification, but nice to have
    To delete simply remove 'mixins.ListModelMixin' from the class definition
    Allows posting: POST /rate/{id:int}/

    Attributes:
        queryset:          Looks through all the Rating objects in the DB
        serializer_class:  Provides a default serializer for the class
    """

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def create(self, request, *args, **kwargs):
        """
        Override the POST method to allow us to calculate
        the average rating of a given car on the fly
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Send update request to parent Car object
            parent_car = Car.objects.get(id=request.data["car_id"])
            parent_car.rate(request.data["rating"])
            # Save the rating info
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_404_NOT_FOUND,
            )


class PopularViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that shows the most popular cars
    Allows listing: GET /popular

    Attributes:
        queryset:          Looks through all the Car objects in the DB
                           Descending sort by number of ratings
        serializer_class:  Provides a default serializer for the class
    """

    queryset = Car.objects.all().order_by("-rates_number")
    serializer_class = PopularSerializer
