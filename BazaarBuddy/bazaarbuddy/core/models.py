from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    class Role(models.TextChoices):
        REGULAR = 'Regular', 'Regular'
        MODERATOR = 'Moderator', 'Moderator'
        ADMIN = 'Admin', 'Admin'
    role = models.CharField(choices=Role.choices, default=Role.REGULAR, max_length=50)


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2,default=0,max_digits=6)
    class Condition(models.TextChoices):
        NEW = 'New', 'New'
        LIKE_NEW = 'Like New', 'Like New'
        USED = 'Used', 'Used'
        DAMAGED = 'Damaged', 'Damaged'
    condition = models.CharField(
        max_length=20,
        choices=Condition.choices,
        default=Condition.NEW
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ceated = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Rating(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    productId = models.ForeignKey(Product, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
