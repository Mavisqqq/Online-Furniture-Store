from django.urls import path
from furniture.views import *

urlpatterns = [
    path('', index, name='Home'),
    path('contacts/', contacts, name='contacts'),
    path('about_us/', about_us, name='about_us'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('catalog/', catalog, name="catalog"),

    path('view_product/<str:slug>/', ViewProduct.as_view(), name='view_product'),
    path('view_product/<str:slug>/remove_from_favorite/', remove_from_favorite_view_product, name='remove_from_favorite_view_product'),
    path('add_review/<str:slug>/', AddReview.as_view(), name='add_review'),

    path('favorites/', favorites, name='favorites'),
    path('favorites/<str:slug>/remove/', remove_from_favorite_favorite, name='remove_from_favorite_favorite'),
    path('favorites/<str:slug>/add_to_favorite/', add_to_favorite, name='add_to_favorite'),

    path('cart/', cart, name='cart'),
    path('cart/<str:slug>/add_favorite/', add_to_cart_favorite, name='add_to_cart_favorite'),
    path('cart/<str:slug>/remove_favorite/', remove_from_cart_favorite, name='remove_from_cart_favorite'),
    path('cart/<str:slug>/add_view_product/', add_to_cart_view_product, name='add_to_cart_view_product'),
    path('cart/<str:slug>/remove_view_product/', remove_from_cart_view_product, name='remove_from_cart_view_product'),
    path('cart/<str:slug>/remove_cart/', remove_from_cart_cart, name='remove_from_cart_cart'),

    path('search/', Search.as_view(), name="search"),
    path('products_by_category/<str:slug>/', ProductByCategory.as_view(), name='products_by_category'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
