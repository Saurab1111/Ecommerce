from django.shortcuts import render
from .models import Product,Order,Reviews
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView
from .serializers import ProductSerializer,OrderSerializer,ReviewSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from .tasks import create_order
from .services.review_analysis import analyze_reviews

class ProductList(APIView):
    def get(self,request):
        objects=Product.objects.all()
        if objects:
            serializer= ProductSerializer(objects,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response("No product Available")
    
    def post(self,request):
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response("Invalid entry",status=status.HTTP_204_NO_CONTENT)

class ProductDetail(RetrieveUpdateDestroyAPIView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        print(slug,"slug")
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found")
    serializer_class=ProductSerializer

class OrderList(ListCreateAPIView):
    # permission_classes=AuthUser #only logged in user can place order (But we are already validating)
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()  #must do else serializer don't have request and all if we override serializer context
        context['slug'] = self.request.query_params.get('slug')
        context['user_id'] = self.request.user_sub
        print(context['slug'])
        return context
    
    def perform_create(self, serializer):
        slug=self.kwargs.get('slug')
        product=Product.objects.get(slug=slug)
        if product.quantity_available>0:
            serializer=ProductSerializer(data=self.request.data)
            if serializer.is_valid():
                create_order.delay(dict(self.request.data))
                return Response(f"We recieved order for {product.name}",status=status.HTTP_201_CREATED)
            else:
                return Response(f"Order not booked please provide details",status=status.HTTP_204_NO_CONTENT)

            

class OrderDetails(RetrieveUpdateDestroyAPIView):
    try:
        def get_object(self):
            track_number=self.kwargs.get('track_number')
            return Order.objects.get(track_number=track_number)
    except Order.DoesNotExist:
        raise NotFound(detail='No such order')
    
    serializer_class=OrderSerializer


class ReviewListCreateView(APIView):

    def get(self, request, slug):
        """
        Get all reviews for a product
        """
        product = Product.objects.get(slug=slug)
        reviews = Reviews.objects.filter(product=product)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, slug):
        """
        Add a new review for a product
        """
        product = Product.objects.get(slug=slug)
        data = request.data.copy()
        data["product"] = product.slug

        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewAnalysisView(APIView):

    def post(self, request, slug):
        product = Product.objects.get(slug=slug)
        analysis = analyze_reviews(product)

        if not analysis:
            return Response(
                {"message": "No reviews available for analysis"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "product": product.name,
            "average_rating": analysis.average_rating,
            "overall_sentiment": analysis.overall_sentiment,
            "review_summary": analysis.review_summary,
            "pros": analysis.pros,
            "cons": analysis.cons,
            "total_reviews": analysis.total_reviews,
        })