from django.urls import path


from . import views

urlpatterns = [
    path("products/", views.products_list),
    path("product/<int:pk>/", views.product_detail),
    path("category/", views.category_list),
    path("categories/<int:pk>/", views.category_detail, name="category_detail"),
]