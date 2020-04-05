from django.urls import path
from .views import item_list, home, checkout
app_name = 'core'

urlpatterns = [
    path('', home),
    path('checkout/', checkout),
    path('products/', item_list)
]
