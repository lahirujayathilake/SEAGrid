from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_seagrid_data_product, name="create-seagrid-data-product"),
]