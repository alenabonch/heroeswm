# -*- coding: utf-8 -*-
from grab.spider import Spider, Task
from lxml import etree
from HWM.heroes.models import *
from datetime import datetime

def str_to_date(text):
    return datetime.strptime(text,'%d-%m-%y %H:%M')

def find_substr(text,beg,end):
    try:
        index = text.find(beg)
        s =''
        index +=1
        while True:
            if(text[index]==end):
                break
            else:
                s+=text[index]
                index+=1
        return s
    except IndexError:
        print text

def find_number(text):
    i = 0
    while True:
        if(text[i].isdigit()):
            break
        else:
            i+=1
    return i

class Graber(Spider):
    initial_urls = ['http://heroeswm.ru/']
    
    def task_initial(self, grab, task):
        self.curr_date = None
        self.limit_date = DateValue.objects.get(pk=1)
        grab.set_input('login','Stats_Graber')
        grab.set_input('lreseted','1')
        grab.set_input('pass','Spider123')
        grab.set_input('preseted','1')
        grab.submit(make_request=False)
        yield Task('login',grab=grab)
        
    def task_login(self, grab, task):
        grab.setup(url='http://www.heroeswm.ru/sklad_log.php?id=12')
        yield Task('store',grab=grab)

    def task_store(self,grab,task):
        html = etree.tostring(grab.xpath('//center/table/tr/td'), encoding='cp1251')
        html = html.decode("cp1251")
        html = html[49:-10]
        logs = html.split('<br/>')
        logs.pop(0)
        logs.pop(0)
        new_page = True
        for log in logs:
            ind = find_number(log)
            date = log[ind:ind+14]
            date = str_to_date(date)
            if(self.curr_date==None):
                self.curr_date = date
            if(date < self.limit_date.date):
                new_page=False
                date_value = DateValue()
                date_value.date = date
                date_value.save()
                break
            index = log.rfind('<!--')
            id = log[index+4:-3]
            if(id=='0'):
                continue
            description = log[ind+16:index]
            description = description[:9]+'http://www.heroeswm.ru/'+description[9:]
            try:
                artifact = Artifact.objects.get(pk=id)
                if(artifact.last_date < date):
                    artifact.last_date = date
                    artifact.strength = find_substr(description,'[',']')
            except Artifact.DoesNotExist:
                artifact = Artifact()
                artifact.id = id
                artifact.name = find_substr(description,"'","'")
                artifact.last_date = date
                artifact.strength = find_substr(description,'[',']')
            artifact.save()
            logObject = Log()
            logObject.artifact=artifact
            logObject.date = date
            logObject.description = description
            logObject.save()
        if(new_page):
            url = task.get('url')
            pageIndex = url.find('page=')
            if(pageIndex!=-1):
                page = int(url[pageIndex+5:])
            else:
                page = 0
            page +=1
            grab.setup(url='http://www.heroeswm.ru/sklad_log.php?id=12&page='+str(page))
            yield Task('store',grab=grab)