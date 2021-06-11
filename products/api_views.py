from django.conf import settings

from django_filters.rest_framework import DjangoFilterBackend
from re import I
import re
from .pagination import CustomPagination
from django.db.models.query import QuerySet
from rest_framework import views
from rest_framework import generics

from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, ProductImages
from .serializers import ProductSerializers
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination





class ProductApiView(views.APIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    pagination_class= CustomPagination

    def get(self, request, format=None):
        category_name = request.GET.get("category", None)
        search = request.GET.get("search", None)

        print(category_name,search)
        try:
            if category_name and search:
                category = Category.objects.get(name=category_name)
                query = Product.objects.filter(
                    category=category.id, name__startswith=search)
                page = self.paginate_queryset(query)
                if page is not None:
                    serializer = self.serializer_class(page, many=True)
                    return self.get_paginated_response(serializer.data)

            elif category_name:

                category = Category.objects.get(name=category_name)
                query = Product.objects.filter(category=category.id)
                page = self.paginate_queryset(query)
                if page is not None:
                    serializer = self.serializer_class(page, many=True)
                    return self.get_paginated_response(serializer.data)
            elif search:

                query = Product.objects.filter(name__startswith=search)
                page = self.paginate_queryset(query)
                if page is not None:
                    serializer = self.serializer_class(page, many=True)
                    return self.get_paginated_response(serializer.data)

            else:
                query = Product.objects.all()
                page = self.paginate_queryset(query)
                if page is not None:
                    serializer = self.serializer_class(page, many=True)
                    return self.get_paginated_response(serializer.data)

                # serializer = ProductSerializers(query, many=True)
                # return Response(serializer.data)
        except Exception as e:
            return Response(status=404)

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator
    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)
    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class PrdoucttDetailApiView(views.APIView):

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializers(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializers(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filterset_fields = ['category__name', 'price']

    filter_backends = [DjangoFilterBackend]


