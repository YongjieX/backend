import graphene
from graphene_django import DjangoObjectType
import time
from customers.models import Customer, Order


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = '__all__'


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = '__all__'


class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    orders = graphene.List(OrderType)
    customer_by_name = graphene.List(
        CustomerType, name=graphene.String(required=True))

    def resolve_customers(root, info):
        return Customer.objects.all()

    def resolve_orders(root, info):
        return Order.objects.select_related('customer').all()

    def resolve_customer_by_name(root, info, name):
        try:
            return Customer.objects.filter(name=name)
        except Customer.DoesNotExist:
            return None


class CreateCustomer(graphene.Mutation):

    class Arguments:
        name = graphene.String()
        industry = graphene.String()

    customer = graphene.Field(CustomerType)

    def mutate(root, info, name, industry):
        customer = Customer(name=name, industry=industry)
        customer.save()
        return CreateCustomer(customer=customer)


class CreateOrder(graphene.Mutation):
    class Arguments:
        description = graphene.String()
        total_in_cents = graphene.Float()
        customer = graphene.ID(required=True)

    order = graphene.Field(OrderType)

    def mutate(root, info, description, total_in_cents, customer):
        try:
            # Retrieve the customer instance
            customer_instance = Customer.objects.get(pk=customer)
        except Customer.DoesNotExist:
            # Handle the case where the customer doesn't exist
            raise Exception("Customer with the given ID does not exist.")
        order = Order(description=description,
                      total_in_cents=total_in_cents, customer=customer_instance)
        # customer = Customer(name=name, industry=industry)
        order.save()
        return CreateOrder(order=order)


class DeleteOrder(graphene.Mutation):
    class Arguments:
        order_id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    order = graphene.Field(OrderType)

    def mutate(root, info, order_id):
        try:
            order = Order.objects.get(pk=order_id)
            order.delete()
            return DeleteOrder(success=True, message="Order deleted successfully.")
        except Order.DoesNotExist:
            return DeleteOrder(success=False, message="Order not found.")


class Mutations(graphene.ObjectType):
    time.sleep(1)
    create_customer = CreateCustomer.Field()
    create_order = CreateOrder.Field()
    delete_order = DeleteOrder.Field()
    # Other mutations as necessary


schema = graphene.Schema(query=Query, mutation=Mutations)
