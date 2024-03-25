from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product


class ProductDetailView(View):
    def get(self, request):
        return render(request, 'task/product/product-list.html')


class ProductSerializer:
    pass


class ProductDetailAPI(APIView):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        product = ProductSerializer(product).data
        return Response(product)