from django.shortcuts import render
class CreateListCouriers(CreateAPIView, ListAPIView):
    serializer_class = CourierSerializer
    queryset = Courier.objects.all()


class TripOfCourier(CreateAPIView):
    serializer_class = TripSerializer

    def perform_create(self, serializer):
        serializer.save(courier_id=self.kwargs.get("pk"))


# Create your views here.
class AdditionalEarningOfCourier(CreateAPIView, ListAPIView):
    serializer_class = AdditionalEarningSerializer

    def perform_create(self, serializer):
        serializer.save(courier_id=self.kwargs.get("pk"))

    def get_queryset(self):
        return (
            AdditionalEarning.objects.filter(date=date.today(), courier_id=self.kwargs.get("pk"))
            .select_related('courier').all()
        )
