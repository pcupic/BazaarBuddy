from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, default=0, max_digits=6)
    image_url = models.CharField(max_length = 512)
    class Condition(models.TextChoices):
        NEW = 'New', 'New'
        LIKE_NEW = 'Like New', 'Like New'
        USED = 'Used', 'Used'
        DAMAGED = 'Damaged', 'Damaged'
    condition = models.CharField(
        max_length=20,
        choices=Condition.choices   
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class State(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        ACCEPTED = 'Accepted', 'Accepted'
        REJECTED = 'Rejected', 'Rejected'
    
    state = models.CharField(
        max_length=20,
        choices=State.choices,
        default=State.PENDING
    )

    def __str__(self):
        return self.title
    
    def average_rating(self):
        ratings = self.rating_set.all() 
        if ratings.exists():
            return sum(rating.grade for rating in ratings) / ratings.count()
        return 0  


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    class Meta:
        unique_together = ('user', 'product')
