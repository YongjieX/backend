
from django.http import JsonResponse, Http404
from .serializer import CustomerSerializer
from rest_framework.decorators import api_view  # which method is allowed
from rest_framework.response import Response
# json/ 404/ html response
from rest_framework import status  # give us a bunch of options of status codes
from .models import Customer  # Assuming your models are in the same app


@api_view(['GET', 'POST'])
def customers(request):
    if request.method == 'GET':

        data = Customer.objects.all()
        serializer = CustomerSerializer(data, many=True)

        # Return the serialized data as JSON response
        return Response({'customers': serializer.data})
    elif request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'customer': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def customer(request, id):
    try:
        data = Customer.objects.get(pk=id)

    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomerSerializer(data)
        return Response({'customer': serializer.data})

    elif request.method == 'DELETE':
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'POST':
        serializer = CustomerSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'customer': serializer.data})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
