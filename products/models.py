from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    name= models.CharField(max_length=100)
    description=models.CharField(max_length=2000)
    slug=models.SlugField(   #slug is just inheritance of CharField hence default is ""
        max_length=200,
        unique=True,
        blank=True,
    )
    price=models.IntegerField()
    is_available= models.BooleanField()
    quantity_available= models.IntegerField()
    product_image=models.URLField()
    review_summary = models.TextField(null=True, blank=True)
    overall_sentiment = models.CharField(max_length=100, null=True, blank=True)
    average_rating = models.FloatField(null=True, blank=True)
    pros = models.CharField(max_length=100,null=True, blank=True)
    cons = models.CharField(max_length=100,null=True, blank=True)
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        else:
            base_slug=slugify(self.name)
            count=0
            while Product.objects.filter(slug=base_slug).exists():
                count+=1
                base_slug+=str(count)
            self.slug=base_slug
        super().save(*args,**kwargs)
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user_id=models.CharField(max_length=100)
    total_payment=models.DecimalField(decimal_places=10,max_digits=20)
    order_data=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20)
    last_updated=models.DateTimeField(auto_now=True)
    track_number=models.BigIntegerField()
    shipping_address=models.TextField()

    # def __str__(self):
    #     return self.product.name+" order"

class Reviews(models.Model):
        product=models.ForeignKey(Product,on_delete=models.CASCADE)
        user=models.CharField(max_length=100)
        review=models.TextField()
        rating=models.IntegerField(validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ])
        rated_date=models.DateTimeField(auto_now_add=True)
        last_updated=models.DateTimeField(auto_now=True)

class ReviewAnalysis(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="analysis"
    )

    average_rating = models.FloatField()
    overall_sentiment = models.CharField(max_length=50)
    review_summary = models.TextField()
    pros = models.TextField()
    cons = models.TextField()

    total_reviews = models.IntegerField()
    last_analyzed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analysis for {self.product.name}"

