from django.urls import path
from . import views

# url that is linked to specified files
urlpatterns = [
    path('', views.home, name='home'),
    path('s/', views.search, name='search'),
    path('menu/', views.menu, name='menu'),
    path('order/', views.order, name='order'),
    path('orders/', views.order_2, name='order_2'),
    path('checkout/', views.checkout, name='checkout'),
    path('menu/<slug>/', views.food, name='food'),
    path('order/<slug>/', views.update_cart, name='update_cart'),
    path('contact/us/', views.contact, name='contact'),
    path('about/us/', views.about, name='about'),
    path('accounts/logout/', views.logout_view, name='auth_logout'),
    path('accounts/login/', views.login_view, name='auth_login'),
    path('accounts/register/', views.registration_view, name='auth_register'),
    path('accounts/activate/<activation_key>/', views.activation_view, name='activation_view'),
]

