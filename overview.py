import kivy
import time

from yweather import YWeather

from kivy.uix.image import Image, AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

class Overview(GridLayout):
    
    def __init__(self, **kwargs):
        super(Overview, self).__init__(**kwargs)

        self.cols = 2
        
        self.dateTimeTile = Label(text = '[b][color=#00ffff]' + self.__getDateTime() + '[/color][/b]', font_size='32sp', markup = True)
        self.add_widget(self.dateTimeTile)
        
        self.weatherTile = WeatherTile()    
        self.add_widget(self.weatherTile)
        
        self.appointmentTile = AppointmentTile()
        self.add_widget(self.appointmentTile)
        
        self.reminderTile = ReminderTile()
        self.add_widget(self.reminderTile)
        
    def __getDateTime(self):
        currentDay = time.strftime("%A")
        #dayToGermanDayMap = {'Monday': 'Montag', 'Tuesday': 'Dienstag', 'Wednesday': 'Mittwoch', 'Thursday': 'Donnerstag', 'Friday': 'Freitag', 'Saturday': 'Sonnabend', 'Sunday': 'Sonntag'}
        #germanDay = dayToGermanDayMap.get(currentDay)
        #formattedDateTime = germanDay + ', ' + time.strftime("%d.%m.%Y %I:%M")
        formattedDateTime = currentDay + ', \n' + time.strftime("%d.%m.%Y %I:%M")
        return formattedDateTime        
        
    def updateDateTime(self):
        self.dateTimeTile.text = '[b][color=#00ffff]' + self.__getDateTime() + '[/color][/b]'
        
    def updateWeather(self):
        self.weatherTile.clear_widgets()
        self.weatherTile.updateWeather()
    
    def updateAppointmentTile(self, dueAppointments):
        self.appointmentTile.clear_widgets()
        for a in dueAppointments:
            self.appointmentTile.addAppointment(a)
            
    def updateReminderTile(self, dueReminders):
        self.reminderTile.clear_widgets()
        for r in dueReminders:
            self.reminderTile.addReminder(r)
        

class AppointmentTile(GridLayout):
    
    def __init__(self, **kwargs):
        super(AppointmentTile, self).__init__(**kwargs)
    
        self.cols = 4
        self.row_force_default=True
        self.row_default_height=20
        
    def addAppointment(self, appointment):
        self.add_widget(Image(source='pics/clock.png', allow_stretch=True))
        self.add_widget(Label(text= appointment.time, font_size='20sp', halign = 'left', markup = True))
        self.add_widget(Label(text= appointment.title, font_size='20sp', halign = 'left', markup = True)) 
        self.add_widget(Label(text= appointment.member, font_size='20sp', halign = 'left', markup = True))
        
class ReminderTile(GridLayout):
    
    def __init__(self, **kwargs):
        super(ReminderTile, self).__init__(**kwargs)
    
        self.cols = 2
        self.row_force_default=True
        self.row_default_height=20
        
    def addReminder(self, reminder):
        self.add_widget(Image(source='pics/birne.png', allow_stretch=True))
        self.add_widget(Label(text= reminder.text, font_size='20sp', halign = 'left', markup = True))
        
class WeatherTile(GridLayout):
    
    def __init__(self, **kwargs):
        super(WeatherTile, self).__init__(**kwargs)
    
        self.cols = 2
        #self.row_force_default=True
        #self.row_default_height=20
        
    def updateWeather(self):
        self.weather = YWeather()
        self.add_widget(Label(text=u'' + self.weather.temp + unichr(176) + 'C', font_size='32sp', markup = True))
        self.add_widget(AsyncImage(source=self.weather.picUrl))
        self.add_widget(Label(text=u'' + self.weather.low + unichr(176) + 'C', font_size='16sp', valign = 'top', markup = True))
        self.add_widget(Label(text=u'' + self.weather.high + unichr(176) + 'C', font_size='16sp', valign = 'top', markup = True))