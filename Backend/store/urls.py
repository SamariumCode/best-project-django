from django.urls import path


from . import views

urlpatterns = [
    path("products/", views.products_list),
    path("product/<int:id>/", views.product_detail),
]