from django.shortcuts import render
from django.conf import settings
from django.views import View
from .models import Slider
from django.db.models import Q

counter = 0
def media_admin(request):
    return {"media_url":settings.MEDIA_URL}

def index(request):
    global counter
    counter += 1
    return render(request,"main_app/index.html",{'counter': counter})


class SliderView(View):
    def get(self, request):
        sliders=Slider.objects.filter(Q(is_active=True))
        return render(request,"main_app/sliders.html",{"sliders":sliders})
    
def ErrorHandler404(request, exception=None):                       # age user to url addresse eshtebah bezane in page ro neshun mide. negah kon shop=> urls.py=> handler404. settings.py => DEBUG=False, ALLOWED_HOSTS = ['*']
    return render(request,"main_app/404.html")
