from django.shortcuts import render
class CreateListCouriers(CreateAPIView, ListAPIView):
    serializer_class = CourierSerializer
    queryset = Courier.objects.all()


class TripOfCourier(CreateAPIView):
    serializer_class = TripSerializer

    def perform_create(self, serializer):
        serializer.save(courier_id=self.kwargs.get("pk"))


# Create your views here.
