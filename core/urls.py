from django.urls import path
from .views import ItemDetailView, HomeView, checkout, item_list
app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', checkout, name='checkout'),
    path('products/', item_list, name='products'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product')
]
