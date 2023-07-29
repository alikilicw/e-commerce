from django.urls import path
from . import views

urlpatterns = [
    path("product-detail/<slug:slug>", views.productDetail, name="productDetailPage"),
    path("product-detail/<slug:slug>/product-comments", views.comments, name="productCommentPage"),
    path("product-detail/<slug:slug>/seller-comments", views.comments, name="sellerCommentPage"),
    path('product-detail/review/<str:review_type>', views.review_saver),
    path("category=<slug:slug>", views.products, name="productsPage"),
    path('search/search-word=<str:search_word>', views.search_product_company, name="searchProductCompany"),
    path('search/search-word=<str:search_word>/filter', views.search_product_company, name="searchProductCompanywFilters"),
    path('filter/<str:country_word>/<str:city_word>/<str:district_word>', views.location_auto_complete, name="locationAutoComplete"),
    path("favorites", views.favorites, name="favoritesPage"),
    path("add-favorites/<slug:slug>", views.addfavorites),
    path("discard-favorites/<slug:slug>", views.discardfavorites),
    path("add-product", views.add_product, name="add-product")
]