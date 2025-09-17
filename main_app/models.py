from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    genre = models.CharField(max_length=100)
    release_year = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    image = models.URLField(max_length=800, default="static/images/ctrlPlay.png")

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("game_detail", kwargs={"game_id": self.id})
    
class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)] 

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Meta:
    unique_together = ("game", "user")  # one review per user per game

    def __str__(self):
        return f"{self.user.username} rated {self.game.title} {self.rating}/5"
    
class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wishlist")
    games = models.ManyToManyField("Game", related_name="wishlisted_by", blank=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"
        
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    games = models.ManyToManyField("Game", related_name="in_carts", blank=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"
    
    def total_price(self):
        return sum(game.price for game in self.games.all())
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    games = models.ManyToManyField("Game", related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"Order #{self.id} by {self.user.username}"

def total_price(self):
    return sum(game.price for game in self.games.all())
    

    

     

    

    

