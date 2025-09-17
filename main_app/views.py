from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Game, Cart, Order, Wishlist
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import ReviewForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

# Create your views here.
class Home(LoginView):
    template_name = "home.html"

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    reviews = game.reviews.all() 

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.game = game
            review.user = request.user
            review.save()
            return redirect("game_detail", game_id=game.id)
    else:
        form = ReviewForm()

    context = {
        "game": game,
        "reviews": reviews,
        "form": form,
    }
    return render(request, "games/detail.html", context)

class GameCreate(LoginRequiredMixin, CreateView):
    model = Game
    fields = ["title", "description", "genre", "release_year", "price", "image"]

    def form_valid(self, form):
        
        form.instance.user = self.request.user  
        return super().form_valid(form)

class GameUpdate(UpdateView):
    model = Game
    fields = ["title", "description", "genre", "release_year", "price", "image"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        game = self.get_object()
        return game.user == self.request.user

class GameDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Game
    success_url = reverse_lazy('game_index')  # redirect after deletion

    def test_func(self):
        # Only allow the owner to delete this game
        game = self.get_object()
        return game.user == self.request.user

@login_required
def game_index(request):
    games = Game.objects.all()
    return render(request, "games/index.html", {"games": games})

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():

            user = form.save()
         
            login(request, user)
            return redirect('game_index')
        else:
            error_message = 'Invalid sign up - try again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == "POST":
        action = request.POST.get("action")
        game_id = request.POST.get("game_id")
        game = get_object_or_404(Game, id=game_id)

        if action == "add" and game not in cart.games.all():
            cart.games.add(game)

        elif action == "remove" and game in cart.games.all():
            cart.games.remove(game)

        return redirect("cart_detail") 

    return render(request, "cart/detail.html", {"cart": cart})

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    if cart.games.exists():  # only create order if cart has games
        order = Order.objects.create(user=request.user)
        order.games.set(cart.games.all())
        cart.games.clear()

    return redirect("orders_index")

@login_required
def orders_index(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, "orders/index.html", {"orders": orders})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/detail.html", {"order": order})

def wishlist_index(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if request.method == "POST":
        game_id = request.POST.get("game_id")
        action = request.POST.get("action")
        game = get_object_or_404(Game, id=game_id)

        if action == "add" and game not in wishlist.games.all():
            wishlist.games.add(game)
        elif action == "remove" and game in wishlist.games.all():
            wishlist.games.remove(game)

        return redirect("wishlist_index")

    return render(request, "wishlist/index.html", {"wishlist": wishlist})
 
