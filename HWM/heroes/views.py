from HWM.utils.Graber import Graber
from HWM.heroes.models import *
from datetime import datetime
from django.http import HttpResponse

def collect_stats(request):
    spider = Graber()
    spider.run()
    return HttpResponse("DONE")