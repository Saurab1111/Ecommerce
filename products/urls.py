from django.urls import path
from .views import (
    ProductDetail,
    ProductList,
    OrderList,
    OrderDetails,
    ReviewListCreateView,
    ReviewAnalysisView,
)


urlpatterns = [
    
    path('all-products/', ProductList.as_view(), name='product-list'),
    path('product_detail/<slug:slug>/', ProductDetail.as_view(), name='product-detail'),
    
    path('orders/', OrderList.as_view()),
    path('orders/<int:track_number>/', OrderDetails.as_view()),

    path('<slug:slug>/reviews/', ReviewListCreateView.as_view(), name='review-list'),
    path('<slug:slug>/reviews/analyze/', ReviewAnalysisView.as_view(), name='review-analysis'),

]
