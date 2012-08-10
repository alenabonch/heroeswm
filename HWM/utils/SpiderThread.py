import threading
import time
from datetime import datetime
from HWM.utils.Graber import Graber
from HWM.heroes.models import DateValue

class SpiderThread(threading.Thread):
    
    def run(self):
        while True:
            date = datetime.now()
            if(date.hour==4):
                spider = Graber()
                spider.run()
            time.sleep(3600)
            