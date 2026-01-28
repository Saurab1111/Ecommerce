from rest_framework import serializers
from .models import Product, Order, Reviews
from datetime import datetime


class ProductSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Product

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        reviews = [x for x in instance.reviews_set.all().values()]
        rep["reviews"] = reviews
        return rep


class OrderSerializer(serializers.ModelSerializer):
    product = serializers.HyperlinkedRelatedField(
        view_name="product-detail",
        lookup_field="slug",
        read_only=True,
    )
    user = serializers.StringRelatedField(read_only=True)
    track_number = serializers.IntegerField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Order

    def create(self, validated_data):
        product = Product.objects.get(slug=self.context["slug"])
        user = self.context["user"]

        if product.quantity_available > 0:
            validated_data["user"] = user
            validated_data["product"] = product

            now = datetime.now()
            track_number = now.strftime("%d%m%Y%H%M%S")
            validated_data["track_number"] = int(track_number)

            order = Order.objects.create(**validated_data)
            product.quantity_available -= 1
            product.save(update_fields=["quantity_available"])
            return order
        else:
            raise serializers.ValidationError("Not enough stock.")


class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Product.objects.all(),
    )
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Reviews
        fields = "__all__"
        read_only_fields = ["rated_date", "last_updated", "user"]