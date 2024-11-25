from kivy.app import App #temel sınıf
from kivy.uix.boxlayout import BoxLayout #düzenleme sınıfı
from kivy.uix.popup import Popup #popup açmak için
from kivy.uix.label import Label #label göstermek için



alarms = []  # Alarm listesi

class AlarmApp(App):#kivy nin App sınıfını miras aldık kullanmak için
    def build(self):#kivy nin metodu olan build ana düzeni döner
        return MainLayout()#ana düzen mainlayout olmuş

class MainLayout(BoxLayout):
    def add_alarm(self):
        # Yeni alarm eklemek için popup açar
        content = BoxLayout(orientation="vertical")
        content.add_widget(Label(text="Yeni Alarm Eklendi!"))
        popup = Popup(title="Alarm Ekleme", content=content, size_hint=(0.8, 0.4))
        popup.open()
        # Bu alana alarm ekleme fonksiyonları bağlanacak
        alarms.append({"time": "07:00", "label": "Yeni Alarm"})  # Örnek bir alarm

    def list_alarms(self):
        # Alarmları listeleme
        for alarm in alarms:
            print(f"Alarm: {alarm['time']} - {alarm['label']}")

if __name__ == "__main__":
    AlarmApp().run()
