
from django.urls import path
from . import views, api_views

urlpatterns = [
    path("",views.ProductListView.as_view(),name="list_products"),
    path("create/",views.CreateProducts.as_view(),name="create_products"),
    path("product-detail/<str:id>/", views.ProductDetail.as_view(), name="detail_products"),
    path("search/", views.ProductSearch.as_view(), name="search_products"),
    path("add-to-cart/", views.AddToCart.as_view(), name="add_to_cart"),
    path("remove-from-cart/", views.RemoveFromCart.as_view(), name="remove_from_cart"),
    path("check-out/", views.CheckOut.as_view(), name="check_out"),
    path("order-detail/", views.OrderDetailView.as_view(), name="order_detail"),
    path("stripe/", views.HomePageView.as_view(), name="stripe"),

    path("success/", views.SuccessView.as_view(), name="success"),
    path("cancel/", views.CancelView.as_view(), name="cancel"),
    # path('create-payment', views.payment,name="payment"),  # new
    path('config/', views.stripe_config),  # new
    path('create-checkout-session/', views.create_checkout_session),

    # rest api paths 

    path('api-product-list/',api_views.ProductApiView.as_view(),name="api_product_listt"),
    path('api-product/<int:pk>',api_views.PrdoucttDetailApiView.as_view(),name="api_product_detail"),

    path('product-listapi/',api_views.ProductListView.as_view(),name="product_listapi"),
    path("bot",views.ChatBotView.as_view(),name="chatbot"),

    



]

