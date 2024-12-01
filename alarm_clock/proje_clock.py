from debugpy.common.timestamp import current
from docutils.nodes import label
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from plyer import notification
from trio import current_time
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from datetime import datetime, time
from threading import Timer

# Alarm listesi
alarms = []

class Alarm:
    def __init__(self, id, time, label):
        self.id = id
        self.time = time
        self.label = label

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10

        #ses dosyası yükleme
        self.alarm_sound=None#alarm sesi referasnı
        self.alarm_sound=SoundLoader.load(r'C:\Users\yildi\Downloads\Kalbim-Yaralı-Fon-Müziği-♬♫♪-_mp3cut.net_.mp3')
        Clock.schedule_interval(self.check_alarm,1)

        # Yeni Alarm Ekleme Butonu
        add_alarm_button = Button(
            text="Yeni Alarm Ekle",
            size_hint=(1, 0.2)
        )
        add_alarm_button.bind(on_press=self.add_alarm_popup)
        self.add_widget(add_alarm_button)

        # Alarmları Listeleme Butonu
        list_alarms_button = Button(
            text="Alarmları Listele",
            size_hint=(1, 0.2)
        )
        list_alarms_button.bind(on_press=self.show_alarms)
        self.add_widget(list_alarms_button)

        # Alarmları görüntülemek için bir ScrollView ekleyeceğiz
        self.alarms_layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.alarms_layout.bind(minimum_height=self.alarms_layout.setter('height'))  # Hızlıca büyümesini sağlar
        scroll_view = ScrollView(size_hint=(1, None), height=400)
        scroll_view.add_widget(self.alarms_layout)
        self.add_widget(scroll_view)

    def add_alarm_popup(self, instance):
        # Alarm ekleme popup'ı
        popup_layout = BoxLayout(orientation="vertical", spacing=10)
        time_input = TextInput(hint_text="Alarm Zamanı (HH:MM)", size_hint=(1, 0.2))
        label_input = TextInput(hint_text="Alarm Etiketi", size_hint=(1, 0.2))


        add_button = Button(text="Ekle", size_hint=(1, 0.2))
        popup_layout.add_widget(time_input)
        if time_input==int:
            print("istenilen formatta yazıldı")
        else:
            print("istenilen formatta değil")
        popup_layout.add_widget(label_input)
        popup_layout.add_widget(add_button)

        popup = Popup(title="Alarm Ekle", content=popup_layout, size_hint=(0.8, 0.6))
        add_button.bind(on_press=lambda x: self.add_alarm(time_input.text, label_input.text, popup))
        popup.open()

    def add_alarm(self, time, label, popup):
        # Alarm ekleme işlevi
        if time and label:
            new_id = len(alarms) + 1
            alarms.append(Alarm(new_id, time, label))
            print(f"Yeni alarm eklendi: {time} - {label}")
            popup.dismiss()
        else:
            print("Lütfen geçerli bir zaman ve etiket girin.")



    def show_alarms(self, instance):
        # Alarmları listeleme
        self.alarms_layout.clear_widgets()  # Önceki alarmları temizle

        if not alarms:
            self.alarms_layout.add_widget(Label(text="Hiç alarm bulunmuyor."))
        else:
            for alarm in alarms:
                # Alarm bilgilerini gösteren bir BoxLayout
                alarm_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
                alarm_label = Label(text=f"{alarm.time} - {alarm.label}", size_hint_x=0.8)

                #güncelleme butonu
                update_button=Button(text="güncelle", size_hint_x=0.5)
                update_button.bind(on_press=lambda instance:self.update_alarm_popup(alarm))


                # Silme butonu
                delete_button = Button(text="Sil", size_hint_x=0.2)
                delete_button.bind(on_press=lambda instance, alarm_id=alarm.id: self.delete_alarm(alarm_id))

                # Layout'a alarm bilgisi ve silme butonunu ekle artı güncelleme butonu
                alarm_layout.add_widget(alarm_label)
                alarm_layout.add_widget(delete_button)
                alarm_layout.add_widget(update_button)

                # Alarmları ekrana ekle
                self.alarms_layout.add_widget(alarm_layout)
    def play_alarm_sound(self):
        if self.alarm_sound is None:
            self.alarm_sound=SoundLoader.load(r'C:\Users\yildi\Downloads\Kalbim-Yaralı-Fon-Müziği-♬♫♪-_mp3cut.net_.mp3')
            if self.alarm_sound:
                self.alarm_sound.play()
                #ses zaten çalııyorsa yeniden başlatma
            else:
                self.alarm_sound.seek(0)#sesi boşa al
                self.alarm_sound.play()

    def stop_alarm_sound(self):
        if self.alarm_sound:
            self.alarm_sound.stop()
            self.alarm_sound=None

    def delete_alarm(self, alarm_id):
        # Alarmı silme
        global alarms
        alarms = [alarm for alarm in alarms if alarm.id != alarm_id]
        print(f"Alarm silindi: ID {alarm_id}")
        self.show_alarms(None)  # Silme işleminden sonra alarmları tekrar gösterme
        self.stop_alarm_sound()

    def update_alarm_popup(self,alarm):
        popup_layout=BoxLayout(orientation="vertical",spacing=10)
        time_input=TextInput(text=alarm.time,hint_text="yeni zaman(HH:MM)",size_hint=(1,0.2))
        label_input=TextInput(text=alarm.label,hint_text="yeni etiket",size_hint=(1,0.2))

        update_button=Button(text="güncelle",size_hint=(1,0.2))
        popup_layout.add_widget(time_input)
        popup_layout.add_widget(label_input)
        popup_layout.add_widget(update_button)

        popup=Popup(title="alarm güncelle",content=popup_layout,size_hint=(0.8,0.6))

        update_button.bind(on_press=lambda instance:self.update_alarm(alarm,time_input.text,label_input.text,popup))
        popup.open()

    def update_alarm(self, alarm, new_time, new_label, popup):
        # Alarmı güncelle
        if new_time and new_label:
            alarm.time = new_time
            alarm.label = new_label
            print(f"Alarm güncellendi: {alarm.time} - {alarm.label}")
            popup.dismiss()  # Güncelleme tamamlandıktan sonra popup'ı kapat
            self.show_alarms(None)  # Güncellenmiş alarmları göster
        else:
            print("Lütfen geçerli bir zaman ve etiket girin.")

    from datetime import datetime

    def check_alarm(self, dt):
        current_time = datetime.now().strftime("%H:%M")  # Mevcut zamanı al

        for alarm in alarms:  # Tüm alarmları kontrol et
            if alarm.time == current_time:  # Eğer alarm saati ile mevcut saat eşleşiyorsa
                print(f"alarm çalıyor: {alarm.time} - {alarm.label}")  # Alarm bilgisini yazdır
                self.play_alarm_sound()  # Alarm sesini çal

                # Alarm çaldıktan sonra alarmlardan çıkarılabilir
                alarms.remove(alarm)  # Alarm listeden çıkar

    #alarm ses çalma
    def play_alarm_sound(self):
        if self.alarm_sound:
            self.alarm_sound.play()
        else:
            print("Ses dosyası yüklenemedi.")


class AlarmApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    AlarmApp().run()
