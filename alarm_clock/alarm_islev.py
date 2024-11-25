from datetime import time


class Alarm:
    def __init__(self,id,time,label,repeat=None,active=True):
        self.id=id
        self.time=time
        self.label=label
        self.repeat=repeat
        self.active=active

#alarm sınıfının özellikleri tanımlandı

#alarm ekleme
alarms=[]

def add_alarm(time,label,repeat=None):
    new_id=len(alarms)+1 #benzersiz yaptık
    alarm=Alarm(new_id,time,label,repeat)
    alarms.append(alarm)
    print(f"yeni alarm eklendi: {alarm.label} ({alarm.time})")

#alarmları listeleme

def list_alarms():
    if not alarms:
        print("Hiç alarm bulunmuyor.")
    for alarm in alarms:
        status="açık" if alarm.active else "kapalı"
        print(f"[{alarm.id}] {alarm.time} - {alarm.label} ({status})")

#alarm güncelleme

def update_alarm(alarm_id,new_time=None,new_label=None,new_repeat=None):
    for alarm in alarms:
        if alarm.id==alarm_id:
            if new_time:
                alarm.time=new_time
            if new_label:
                alarm.label=new_label
            if new_repeat:
                alarm.repeat=new_repeat
            print(f"Alarm gğncellendi : {alarm.label} ({alarm.time})")
            return
        print("alarm bulunamadı")

#alarm silme

def delete_alarm(alarm_id):
    global alarms
    alarms=[alarm for alarm in alarms if alarm.id !=alarm_id]
    print(f"Alarm silindi: ID {alarm_id}")

#alarm kontrolü

from datetime import datetime
import time

def check_alarms():
    while True:
        now=datetime.now().strftime('%S:%D')
        for alarm in alarms:
            if alarm.time==now and alarm.active:
                print(f"Alarm çalıyor {alarm.label}")
                alarm.active=False #bir kez çalsın
        time.sleep(60) #her dk kontrol

