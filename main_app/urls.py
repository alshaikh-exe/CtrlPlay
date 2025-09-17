from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("about/", views.about, name="about"),
    path("games/", views.game_index, name="game_index"),
    path("games/<int:game_id>/", views.game_detail, name="game_detail"),
    path("games/create/", views.GameCreate.as_view(), name="game_create"),
    path("games/<int:pk>/update/", views.GameUpdate.as_view(), name="game_update"),
    path("games/<int:pk>/delete/", views.GameDelete.as_view(), name="game_delete"),
    path('accounts/signup/', views.signup, name='signup'),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),
]