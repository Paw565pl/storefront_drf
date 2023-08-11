from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)
from django_filters.rest_framework import DjangoFilterBackend
from store.filters import ProductFilter
from store.paginations import StandardSizePagination
from .models import Product, OrderItem, Collection, Review, Cart, CartItem
from .serializers import (
    AddCartItemSerializer,
    CartItemSerializer,
    CartSerializer,
    ProductSerializer,
    CollectionSerializer,
    ReviewSerializer,
    UpdateCartItemSerializer,
)


# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related("promotions").all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]
    pagination_class = StandardSizePagination

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs["pk"]).exists():
            return Response(
                {
                    "error": "Product can not be deleted because it is associated with an order item."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


# class ProductList(APIView):
#     queryset = Product.objects.prefetch_related("promotions").all()
#     serializer_class = ProductSerializer

# def get(self, _):
#     queryset = (
#         Product.objects.select_related("collection")
#         .prefetch_related("promotions")
#         .all()
#     )
#     serializer = ProductSerializer(queryset, many=True)
#     return Response(serializer.data)

# def post(self, request):
#     serializer = ProductSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_201_CREATED)


# class ProductDetail(APIView):
#     queryset = Product.objects.prefetch_related("promotions").all()
#     serializer_class = ProductSerializer

# def get(self, _, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)

# def post(self, request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product, data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_200_OK)

# def patch(self, request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product, data=request.data, partial=True)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_200_OK)

# def delete(self, _, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if OrderItem.objects.filter(product_id=pk).exists():
#         return Response(
#             {
#                 "error": "Product can not be deleted because it is associated with an order item."
#             },
#             status=status.HTTP_405_METHOD_NOT_ALLOWED,
#         )
#     product.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.prefetch_related("product_set").all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        collection = self.get_object()
        if Product.objects.filter(collection=collection).exists():
            return Response(
                {
                    "error": "Collection can not be deleted because it is associated with one or more products."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


# class CollectionList(APIView):
#     queryset = Collection.objects.prefetch_related("product_set").all()
#     serializer_class = CollectionSerializer

# def get(self, _):
#     queryset = Collection.objects.prefetch_related("product_set").all()
#     serializer = CollectionSerializer(queryset, many=True)
#     return Response(serializer.data)

# def post(self, request):
#     serializer = CollectionSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_201_CREATED)


# class CollectionDetail(APIView):
#     queryset = Collection.objects.prefetch_related("product_set").all()
#     serializer_class = CollectionSerializer

# def get(self, _, pk):
#     collection = get_object_or_404(Collection, pk=pk)
#     serializer = CollectionSerializer(collection)
#     return Response(serializer.data)

# def put(self, request, pk):
#     collection = get_object_or_404(Collection, pk=pk)
#     serializer = CollectionSerializer(collection, data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_200_OK)

# def patch(self, request, pk):
#     collection = get_object_or_404(Collection, pk=pk)
#     serializer = CollectionSerializer(collection, data=request.data, partial=True)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_200_OK)

# def delete(self, _, pk):
#     collection = get_object_or_404(Collection, pk=pk)
#     if Product.objects.filter(collection=collection).exists():
#         return Response(
#             {
#                 "error": "Collection can not be deleted because it is associated with one or more products."
#             },
#             status=status.HTTP_405_METHOD_NOT_ALLOWED,
#         )
#     collection.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"]).all()

    def get_serializer_context(self):
        return {"product_pk": self.kwargs["product_pk"]}


class CartViewSet(
    GenericViewSet, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
):
    queryset = Cart.objects.prefetch_related("cartitem_set__product").all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        return (
            CartItem.objects.filter(cart_id=self.kwargs["cart_pk"])
            .select_related("product")
            .all()
        )

    def get_serializer_context(self):
        return {"cart_pk": self.kwargs["cart_pk"]}
