from django.shortcuts import render
from .models import Product, Order, Reviews
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .serializers import ProductSerializer, OrderSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from .services.review_analysis import analyze_reviews
from rest_framework.permissions import IsAuthenticated


class ProductList(APIView):
    # Auth required by default (from REST_FRAMEWORK settings)

    def get(self, request):
        objects=Product.objects.all()
        if objects:
            serializer= ProductSerializer(objects,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response("No product Available")
    
    def post(self, request):
        # Only admin users (staff) can create products
        if not request.user.is_staff:
            return Response(
                {"detail": "Only admin users can add products."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    # Only logged-in users can place orders
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()  #must do else serializer don't have request and all if we override serializer context
        context["slug"] = self.request.query_params.get("slug")
        # Pass the full user object into context
        context["user"] = self.request.user if self.request.user.is_authenticated else None
        print(context["slug"])
        return context
    
    def perform_create(self, serializer):
        """
        Create the order synchronously without Celery.
        """
        # Let the serializer.handle creation using its custom create()
        order = serializer.save()
        product = order.product
        return Response(
            {"message": f"We received order for {product.name}", "track_number": order.track_number},
            status=status.HTTP_201_CREATED,
        )

            

class OrderDetails(RetrieveUpdateDestroyAPIView):
    try:
        def get_object(self):
            track_number=self.kwargs.get('track_number')
            return Order.objects.get(track_number=track_number)
    except Order.DoesNotExist:
        raise NotFound(detail='No such order')
    
    serializer_class=OrderSerializer


class ReviewListCreateView(APIView):
    """
    List reviews for a product (GET) and allow only users
    who have purchased the product to create a review (POST).
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        """
        Get all reviews for a product.
        """
        product = Product.objects.get(slug=slug)
        reviews = Reviews.objects.filter(product=product)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, slug):
        """
        Add a new review for a product.
        Only allowed if the authenticated user has bought the product.
        """
        product = Product.objects.get(slug=slug)

        # Check if the user has at least one order for this product
        has_bought = Order.objects.filter(
            product=product,
            user=request.user,
        ).exists()

        if not has_bought:
            return Response(
                {"detail": "You can only review products you have purchased."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data.copy()
        data["product"] = product.slug

        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
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