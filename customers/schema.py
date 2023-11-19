import graphene
from graphene_django import DjangoObjectType

from customers.models import Customer

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = '__all__'


class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    customer_by_name = graphene.List(CustomerType, name=graphene.String(required=True))

    def resolve_customers(root, info):
        return Customer.objects.all()

    def resolve_customer_by_name(root, info, name):
        try:
            return Customer.objects.filter(name=name)
        except Customer.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)