from itertools import product
import graphene

from graphene_django import DjangoObjectType, DjangoListField 
from .models import Product,ProductImages 


class ProductType(DjangoObjectType): 
    class Meta:
        model = Product
        fields = "__all__"


class Query(graphene.ObjectType):
    all_books = graphene.List(ProductType)
    book = graphene.Field(ProductType, product_id=graphene.Int())

    def resolve_all_books(self, info, **kwargs):
        return Product.objects.all()

    def resolve_book(self, info, product_id):
        return Product.objects.get(pk=product_id)


class ProductInput(graphene.InputObjectType):
    id = graphene.ID()
    seller= graphene.ID()
    name = graphene.String()
    description = graphene.String()
    category = graphene.ID()
    price = graphene.Int() 


class CreateProducts(graphene.Mutation):
    class Arguments:
        book_data = ProductInput(required=True)

    book = graphene.Field(ProductType)

    @staticmethod
    def mutate(root, info, book_data=None):
        book_instance = Product( 
            name=book_data.name,
            description=book_data.description,
            category=book_data.category,
            price=book_data.price
        )
        book_instance.save()
        return CreateProducts(book=book_instance)


class UpdateProduct(graphene.Mutation):
    class Arguments:
        book_data = ProductInput(required=True)

    book = graphene.Field(ProductType)

    @staticmethod
    def mutate(root, info, book_data=None):

        book_instance = Product.objects.get(pk=book_data.id)

        if book_instance:
            book_instance. name = book_data.name
            book_instance.description = book_data.description
            book_instance.category = book_data.category
            book_instance.price = book_data.price
            book_instance.save()

            return UpdateProduct(book=book_instance)
        return UpdateProduct(book=None)



class Deleteproduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    book = graphene.Field(ProductType)

    @staticmethod
    def mutate(root, info, id):
        book_instance = Product.objects.get(pk=id)
        book_instance.delete()

        return None


class Mutation(graphene.ObjectType):
    create_book = CreateProducts.Field()
    update_book = UpdateProduct.Field()
    delete_book = Deleteproduct.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)