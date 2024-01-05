from django.shortcuts import render
class CreateListCouriers(CreateAPIView, ListAPIView):
    serializer_class = CourierSerializer
    queryset = Courier.objects.all()

# Create your views here.
