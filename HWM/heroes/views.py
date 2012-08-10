# -*- coding: utf-8 -*-
from HWM.utils.Graber import Graber
from HWM.heroes.models import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from HWM.utils.SpiderThread import SpiderThread

def run_spider():
    thread = SpiderThread()
    thread.start()
    
run_spider()

def index(request):
    return render_to_response('index.html')

def get_broken():
    return Artifact.objects.filter(strength__startswith='0').order_by('name')

def get_not_broken():
    return Artifact.objects.exclude(strength__startswith='0').order_by('name')

def get_by_name(category):
    return Artifact.objects.filter(name__istartswith=category).order_by('name')

def get_alphabet_categories():
    alphabet = u"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    categories = []
    for alpha in alphabet: 
        cat_arts = Artifact.objects.filter(name__istartswith=alpha)
        if(cat_arts.count() > 0):
            categories.append(alpha)
    return categories

def stats(request):
    category = request.GET.get('cat','')
    if category != '':
        cats = {'broken':get_broken, 'notbroken': get_not_broken}
        if(category in cats):
            arts = cats[category]()
        else:
            arts = get_by_name(category)
    else:
        arts = None
   
    return render_to_response('stats.html', {'categories': get_alphabet_categories(), 'arts': arts})

def art_info(request):
    art_id = request.GET.get('id','1')
    try:
        art = Artifact.objects.get(id=art_id)
        logs = art.log_set.order_by('date')
    except Artifact.DoesNotExist:
        art = None
        logs =  []
    return render_to_response('stats.html', {'categories': get_alphabet_categories(), 'artifact': art, 'logs':logs})