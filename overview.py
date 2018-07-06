import kivy
import time

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

class Overview(GridLayout):
    
    def __init__(self, **kwargs):
        super(Overview, self).__init__(**kwargs)

        self.cols = 2
        
        self.dateTimeTile = Label(text = '[b][color=#00ffff]' + self.__getDateTime() + '[/color][/b]', font_size='32sp', markup = True)
        self.add_widget(self.dateTimeTile)
        
        self.add_widget(Label(text='Platzhalter'))
        
        self.appointmentTile = AppointmentTile()
        self.add_widget(self.appointmentTile)
        
        self.add_widget(Label(text='Platzhalter'))
        
    def __getDateTime(self):
        currentDay = time.strftime("%A")
        #dayToGermanDayMap = {'Monday': 'Montag', 'Tuesday': 'Dienstag', 'Wednesday': 'Mittwoch', 'Thursday': 'Donnerstag', 'Friday': 'Freitag', 'Saturday': 'Sonnabend', 'Sunday': 'Sonntag'}
        #germanDay = dayToGermanDayMap.get(currentDay)
        #formattedDateTime = germanDay + ', ' + time.strftime("%d.%m.%Y %I:%M")
        formattedDateTime = currentDay + ', \n' + time.strftime("%d.%m.%Y %I:%M")
        return formattedDateTime        
        
    def updateDateTime(self):
        self.dateTimeTile.text = '[b][color=#00ffff]' + self.__getDateTime() + '[/color][/b]'
        
    def updateAppointmentTile(self, dueAppointments):
        self.appointmentTile.clear_widgets()
        for a in dueAppointments:
            self.appointmentTile.addAppointment(a)     
        

class AppointmentTile(GridLayout):
    
    def __init__(self, **kwargs):
        super(AppointmentTile, self).__init__(**kwargs)
    
        self.cols = 3
        self.row_force_default=True
        self.row_default_height=20
        
    def addAppointment(self, appointment):
        self.add_widget(Label(text= appointment.time))
        self.add_widget(Label(text= appointment.title)) 
        self.add_widget(Label(text= appointment.member))