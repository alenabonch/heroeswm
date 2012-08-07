from HWM.utils.Graber import Graber
from HWM.heroes.models import *
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render_to_response

def collect_stats(request):
    spider = Graber()
    spider.run()
    return HttpResponse("DONE")

def index(request):
    return render_to_response('index.html')