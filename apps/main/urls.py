from django.urls import path
from . import views
from ..products.views import get_cheapest_products                  # .. yani boro birun.

app_name="main"
urlpatterns = [
    path("",views.index, name="index"),
    path("sliders",views.SliderView.as_view(),name="sliders")
]
