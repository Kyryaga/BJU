from django.db import models
from django.contrib.auth.models import AbstractUser


# user model
class User(AbstractUser):  
    weight = models.FloatField() 
    height = models.FloatField()
    calorie_goal = models.IntegerField()
    age = models.IntegerField()

    def __str__(self):
        return self.username
    
    @property
    def rsk(self):
        bmr = 88.36 + (13.4 * self.weight) + (4.8 * self.height) - (5.7 * self.age)
        return bmr * 1.5


class Product(models.Model):
    name = models.CharField(max_length=32)
    calories = models.IntegerField()

    prots = models.FloatField()
    fats = models.FloatField()
    carbos = models.FloatField()

    def __str__(self):
        return f'{self.name}({self.calories}, {self.prots}/{self.fats}/{self.carbos})'
    
class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="diaries")
    date = models.DateField(null=False)
    products = models.ManyToManyField(Product, through="ProductsDiaries")

    def __str__(self):
        return f"Дневник {self.user}({self.date})"
    


# intermediate table Products-Diaries for m-m
class ProductsDiaries(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE, related_name='product_entries')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # weight in grams
    weight = models.IntegerField(default=100)
    

