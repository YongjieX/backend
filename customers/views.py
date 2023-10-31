

from django.http import JsonResponse
from .serializer import CustomerSerializer
from .models import Customer  # Assuming your models are in the same app


def customers(request):
    # Get all Customer objects
    data = Customer.objects.all()
    # Serialize the customer data
    serializer = CustomerSerializer(data, many=True)

    # Return the serialized data as JSON response
    return JsonResponse({'customers':serializer.data}, safe=False)
