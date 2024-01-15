from django.urls import path
from . import views

app_name="products"
urlpatterns = [
    path("cheapest_products/",views.get_cheapest_products,name="cheapest_products"),
    path("last_products/<str:widget>/",views.get_last_products,name="last_products"),           # because we use /str:widget/, in html file we should give it paramtere
    path("most_purchased_products/",views.get_most_purchased_products,name="most_purchased_products"),
    path("popular_productGroups/",views.get_popular_productGroups,name="popular_productGroups"),
    path("ProductDetail/<slug:slug>/",views.ProductDetailView.as_view(),name="ProductDetail"),                # models.py => Product => def get_absolute_url(self)
    path("related_products/<slug:slug>/",views.get_related_products,name="related_products"),                 # product_detail.html => 
    path("product_groups/",views.ProductGroupsView.as_view(),name="product_groups"),
    path("product_groups_partial/",views.get_product_groups,name="product_groups_partial"),
    path("products_of_group/<slug:slug>/",views.ProductsOfGroup.as_view(),name="products_of_group"),
    path("brands_partial/<slug:slug>/",views.get_brands,name="brands_partial"),                         # when we use /<slug:slug>/, in html file we should give it parmater
    path("features_for_filter/<slug:slug>/",views.get_features_for_filter,name="features_for_filter"),
    path("ajax_admin/",views.get_filter_value_for_feature,name="filter_value_for_feature"),
    path("compare_list/",views.showCompareListViw.as_view(),name="compare_list"),
    path("compare_table/",views.compare_table,name="compare_table"),
    path("add_to_compare_list/",views.add_to_compare_list,name="add_to_compare_list"),
    path("status_of_compare_list/",views.status_of_compare_list,name="status_of_compare_list"),
    path("delete_from_compare_list/",views.delete_from_compare_list,name="delete_from_compare_list"),
]
