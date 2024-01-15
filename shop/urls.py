from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("apps.main.urls",namespace="main")),
    path("accounts/",include("apps.accounts.urls",namespace="accounts")),
    path("products/",include("apps.products.urls",namespace="products")),
    path("ckeditor",include("ckeditor_uploader.urls")),
    path("orders/",include("apps.orders.urls", namespace="orders")),
    path("discount/",include("apps.discount.urls", namespace="discount")),
    path("payments/",include("apps.payments.urls", namespace="payments")),
    path("warehouses/",include("apps.warehouses.urls", namespace="warehouses")),
    path("csf/",include("apps.comment_scoring_favorites.urls", namespace="csf")),              # comment_scoring_favorites
    path("search/",include("apps.search.urls", namespace="search")),
    path("test_api/",include("apps.test_api.urls", namespace="test_api")),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = "apps.main.views.ErrorHandler404"                          # handler404 hatman bayad esmesh hamin bashe. age user to url addresse eshtebah bezane in page ro neshun mide. settings.py => DEBUG=False, ALLOWED_HOSTS = ['*']