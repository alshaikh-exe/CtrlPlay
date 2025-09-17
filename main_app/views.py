from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Game, Cart, Order, Wishlist
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import ReviewForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
    fields = "__all__"

    def form_valid(self, form):
        
        form.instance.user = self.request.user  
        return super().form_valid(form)

class GameUpdate(UpdateView):
    model = Game
    fields = "__all__"

    

class GameDelete(DeleteView):
    model = Game
    fields = "__all__"
    success_url = "/games/"

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

def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    if not cart.games.exists():
        return redirect("game_index")
    
    order = Order.objects.create(user=request.user)
    order.games.set(cart.games.all())

    cart.games.clear()

    return redirect("order_detail", order_id=order.id)

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/detail.html", {"order": order})

def wishlist_toggle(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if game in wishlist.games.all():
        wishlist.games.remove(game)
    else:
        wishlist.games.add(game)

    return redirect("game_detail", game_id=game.id)

def wishlist_detail(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, "wishlist/detail.html", {"wishlist": wishlist})
 
