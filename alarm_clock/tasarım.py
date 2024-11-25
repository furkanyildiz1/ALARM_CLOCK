from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

alarms = []  # Alarm listesi

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"#vertical ile dikey olarak yerleştirdik
                                    #hoitzontal ile yatay olarak yerleşirdi
        self.padding = 20
        self.spacing = 10

        # Yeni Alarm Ekleme Butonu
        add_alarm_button = Button(
            text="Yeni Alarm Ekle",
            size_hint=(1, 0.2)
        )
        add_alarm_button.bind(on_press=self.add_alarm)
        self.add_widget(add_alarm_button)

        # Alarmları Listeleme Butonu
        list_alarms_button = Button(
            text="Alarmları Listele",
            size_hint=(1, 0.2)
        )
        list_alarms_button.bind(on_press=self.list_alarms)
        self.add_widget(list_alarms_button)

    def add_alarm(self, instance):
        # Yeni alarm eklemek için popup açar
        content = BoxLayout(orientation="vertical")
        content.add_widget(Label(text="Yeni Alarm Eklendi!"))
        popup = Popup(title="Alarm Ekleme", content=content, size_hint=(0.8, 0.4))
        popup.open()
        alarms.append({"time": "07:00", "label": "Yeni Alarm"})  # Örnek bir alarm
        print("Yeni alarm eklendi: 07:00 - Yeni Alarm")

    def list_alarms(self, instance):
        # Alarmları listeleme
        if not alarms:
            print("Alarm bulunamadı.")
        else:
            for alarm in alarms:
                print(f"Alarm: {alarm['time']} - {alarm['label']}")

class AlarmApp(App):
    def build(self):
        return MainLayout()

if __name__ == "__main__":
    AlarmApp().run()
