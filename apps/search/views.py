from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from apps.products.models import Product


class SearchResultsView(View):          # chon page kamel gharare load beshe behtare az classha estefade konim
    def get(self, request, *args, **kwargs):
        query=self.request.GET.get("q")                # injuri ham mishe => query= kwargs["q"]. az url(querystring) dare miyad. name "q" hast, value ro miyare
        products=Product.objects.filter(               # __icontains yani to product namesh in query bashe.
            Q(product_name__icontains=query) |                      # | or
            Q(description__icontains=query)
            )
        
        context={
            "products":products
        }
        
        return render(request,"search_app/search_results.html",context)