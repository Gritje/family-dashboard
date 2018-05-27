import sqlite3
import kivy

from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.garden.datetimepicker import DatetimePicker
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

from functools import partial

class Appointments(BoxLayout):
    
    def __init__(self, **kwargs):
        super(Appointments, self).__init__(**kwargs)
        
        self.orientation='vertical'
        
        self.newAppointmentButton = Button(text='Neuer Termin...', size=(200, 100), size_hint=(None, None), font_size=14)
        
        self.popupLayout = BoxLayout(orientation = 'vertical')        
        self.datetimePicker = DatetimePicker()
        self.appointmentTitleInput = TextInput(text='Neuer Termin:', multiline=False)
        self.memberLayout = BoxLayout(orientation='horizontal')       
        self.memberButton1 = ToggleButton(text='Papa', group='members', state='down')
        self.memberButton2 = ToggleButton(text='Mama', group='members')
        self.memberButton3 = ToggleButton(text='Fiete', group='members')
        self.memberButton4 = ToggleButton(text='Oma', group='members')
        self.memberLayout.add_widget(self.memberButton1)
        self.memberLayout.add_widget(self.memberButton2)
        self.memberLayout.add_widget(self.memberButton3)
        self.memberLayout.add_widget(self.memberButton4)      
        self.saveButton = Button(text='Speichern')
        self.popupLayout.add_widget(self.datetimePicker)
        self.popupLayout.add_widget(self.appointmentTitleInput)
        self.popupLayout.add_widget(self.memberLayout)
        self.popupLayout.add_widget(self.saveButton)
        self.popup = Popup(title='Was?', content=self.popupLayout, auto_dismiss=False)
        self.popup.bind(on_dismiss=partial(self.newAppointmentCallback, self.datetimePicker.get_datetime()))
        self.saveButton.bind(on_press=self.popup.dismiss)
        self.newAppointmentButton.bind(on_press=self.popup.open)
        self.add_widget(self.newAppointmentButton)
        
        self.grid = GridLayout(cols = 4)
        self.grid.row_force_default=True
        self.grid.row_default_height=40
        self.add_widget(self.grid)  
        self.refreshData()        

    def refreshData(self):
        connection = sqlite3.connect("dashboard.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Appointment ORDER BY appdate DESC")

        self.remove_widget(self.grid)
        self.grid = GridLayout(cols = 4)
        self.grid.row_force_default=True
        self.grid.row_default_height=40
        self.add_widget(self.grid)        
        
        for row in cursor:
             self.grid.add_widget(Label(text= str(row[1]) + ' ' + str(row[2]))) #date time
             self.grid.add_widget(Label(text= str(row[3]))) #appointment
             self.grid.add_widget(Label(text= str(row[4]))) #family member
             deleteButton = Button(text='[color=#ff0000]X[/color]', markup = True)
             deleteButton.bind(on_press=partial(self.deleteAppointmentCallback, row[0])) #id 
             self.grid.add_widget(deleteButton)

        connection.close()
     
    def deleteAppointmentCallback(self, rowId, *args):
        connection = sqlite3.connect("dashboard.db")
        cursor = connection.cursor()
        sql = "DELETE FROM Appointment WHERE id = " + str(rowId)
        print("SQL: " + sql)
        cursor.execute(sql)
        connection.commit()
        connection.close()
        self.refreshData()

    def newAppointmentCallback(self, appointmentTime, *args):
        appointmentTime = self.datetimePicker.get_datetime()
        connection = sqlite3.connect("dashboard.db")
        cursor = connection.cursor()
        date = str(appointmentTime.strftime("%Y-%m-%d")) # 2018-05-15
        time = str(appointmentTime.strftime("%H:%M")) # 16:00
        appointment = self.appointmentTitleInput.text
        member = 'Fiete'
        sql = "INSERT INTO Appointment(appdate, apptime, apptext, member) VALUES(date('"+str(date)+"'), time('"+str(time)+"'), '" + appointment + "', '" + member + "')"
        print("SQL: " + sql)
        cursor.execute(sql)
        connection.commit()
        connection.close()
        self.refreshData()