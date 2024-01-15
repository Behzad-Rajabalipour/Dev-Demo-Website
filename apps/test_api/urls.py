from django.urls import path
from . import views

app_name="test_api"
urlpatterns = [
    path("products/",views.AllPoductsApi.as_view(),name="products")
]
