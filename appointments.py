import sqlite3
import time
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
from kivy.uix.behaviors import ToggleButtonBehavior

from functools import partial

class Appointments(BoxLayout):
    
    def __init__(self, **kwargs):
        super(Appointments, self).__init__(**kwargs)
        
        self.orientation='vertical'
        
        self.newAppointmentButton = Button(text='Neuer Termin...', size=(200, 50), size_hint=(None, None), font_size=14)
        self.newReminderButton = Button(text='Neue Erinnerung...', size=(200, 50), size_hint=(None, None), font_size=14)
                
        self.appointmentPopup = self.__newAppointmentPopup()
        self.newAppointmentButton.bind(on_press=self.appointmentPopup.open)
        self.add_widget(self.newAppointmentButton)
        
        self.reminderPopup = self.__newReminderPopup()
        self.newReminderButton.bind(on_press=self.reminderPopup.open)
        self.add_widget(self.newReminderButton)
        
        self.grid = GridLayout(cols = 4)
        self.grid.row_force_default=True
        self.grid.row_default_height=40
        self.add_widget(self.grid)
        self.__appointmentDates = []
        self.refreshData()
        
    def __newAppointmentPopup(self):
        popupLayout = BoxLayout(orientation = 'vertical')
        
        datetimePicker = DatetimePicker()
        appointmentTitleInput = TextInput(text='Was?', multiline=False)
        memberLayout = BoxLayout(orientation='horizontal')       
        memberButton1 = ToggleButton(text='Papa', group='members', state='down')
        memberButton2 = ToggleButton(text='Mama', group='members')
        memberButton3 = ToggleButton(text='Fiete', group='members')
        memberButton4 = ToggleButton(text='Oma', group='members')
        memberLayout.add_widget(memberButton1)
        memberLayout.add_widget(memberButton2)
        memberLayout.add_widget(memberButton3)
        memberLayout.add_widget(memberButton4)      
        saveButton = Button(text='Speichern')
        
        popupLayout.add_widget(datetimePicker)
        popupLayout.add_widget(appointmentTitleInput)
        popupLayout.add_widget(memberLayout)
        popupLayout.add_widget(saveButton)
        
        popup = Popup(title='Neuer Termin:', content=popupLayout, auto_dismiss=False)
        popup.bind(on_dismiss=partial(self.newAppointmentCallback, datetimePicker.get_datetime(), appointmentTitleInput.text))
        saveButton.bind(on_press=popup.dismiss)
        
        return popup

    def __newReminderPopup(self):
        popupLayout = BoxLayout(orientation = 'vertical')
        
        starttimePicker = DatetimePicker()
        reminderTitleInput = TextInput(text='Was?', multiline=False)
        saveButton = Button(text='Speichern')
        interval = TextInput(text='1', multiline=False)
        popupLayout.add_widget(starttimePicker)
        popupLayout.add_widget(reminderTitleInput)
        popupLayout.add_widget(interval)
        popupLayout.add_widget(saveButton)
        
        popup = Popup(title='Neue Erinnerung:', content=popupLayout, auto_dismiss=False)
        popup.bind(on_dismiss=partial(self.newReminderCallback, starttimePicker.get_datetime(), reminderTitleInput.text, interval.text))
        saveButton.bind(on_press=popup.dismiss)
        
        return popup

    def refreshData(self):
        connection = sqlite3.connect("dashboard.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Appointment ORDER BY appdate DESC")

        self.__appointmentDates = []

        self.remove_widget(self.grid)
        self.grid = GridLayout(cols = 4)
        self.grid.row_force_default=True
        self.grid.row_default_height=40
        self.add_widget(self.grid)        
        
        for row in cursor:
            self.__appointmentDates.append(str(row[1]))
            self.grid.add_widget(Label(text= str(row[1]) + ' ' + str(row[2]))) #date time
            self.grid.add_widget(Label(text= str(row[3]))) #appointment
            name = str(row[4])            
            self.grid.add_widget(Label(text= '[b][color=' + self.getColorForName(name) + ']' + name + '[/color][/b]', markup = True)) #family member
            deleteButton = Button(text='[color=#ff0000]X[/color]', size=(40, 40), size_hint=(None, None), markup = True)
            deleteButton.bind(on_press=partial(self.deleteAppointmentCallback, row[0])) #id 
            self.grid.add_widget(deleteButton)
            
        cursor.execute("SELECT * FROM Reminder ORDER BY startdate DESC")
        
        for row in cursor:
            self.grid.add_widget(Label(text= str(row[1]))) #date
            self.grid.add_widget(Label(text= str(row[2]))) #reminder 
            self.grid.add_widget(Label(text= str(row[3]) + ' Wochen')) #interval in weeks
            deleteReminderButton = Button(text='[color=#ff0000]X[/color]', size=(40, 40), size_hint=(None, None), markup = True)
            deleteReminderButton.bind(on_press=partial(self.deleteReminderCallback, row[0])) #id 
            self.grid.add_widget(deleteReminderButton)            
            
        connection.close()
     
    def getColorForName(self, name):
        nameToColorMap = {'Papa': '#00ffff', 'Mama': '#ff6699', 'Oma': '#ffff00', 'Fiete': '#33cc33'}
        return nameToColorMap.get(name)                
    
    def newAppointmentCallback(self, appointmentTime, appointment, *args):
        connection = sqlite3.connect("dashboard.db")
        cursor = connection.cursor()
        date = str(appointmentTime.strftime("%Y-%m-%d")) # 2018-05-15
        time = str(appointmentTime.strftime("%H:%M")) # 16:00
       
        member = 'Fiete'
        
        memberButtons = ToggleButtonBehavior.get_widgets('members')
        for m in memberButtons:
            if m.state == 'down':
                member = m.text
                break
        
        sql = "INSERT INTO Appointment(appdate, apptime, apptext, member) VALUES(date('"+str(date)+"'), time('"+str(time)+"'), '" + appointment + "', '" + member + "')"
        print("SQL: " + sql)
        cursor.execute(sql)
        connection.commit()
        connection.close()
        self.refreshData()

    def deleteAppointmentCallback(self, rowId, *args):
        connection = sqlite3.connect("dashboard.db")
        cursor = connection.cursor()
        sql = "DELETE FROM Appointment WHERE id = " + str(rowId)
        print("SQL: " + sql)
        cursor.execute(sql)
        connection.commit()
        connection.close()
        self.refreshData()
        
    def newReminderCallback(self, startTime, reminder, intervalInWeeks, *args):
        connection = sqlite3.connect("dashboard.db")
        cursor = connection.cursor()
        dateStr = str(startTime.strftime("%Y-%m-%d")) # 2018-05-15
        
        sql = "INSERT INTO Reminder(startdate, text, interval) VALUES(date('"+ dateStr +"'), '" + reminder + "', " + str(intervalInWeeks) + ")"
        print("SQL: " + sql)
        cursor.execute(sql)
        connection.commit()
        connection.close()
        self.refreshData()
        
    def deleteReminderCallback(self, rowId, *args):
        connection = sqlite3.connect("dashboard.db")
        cursor = connection.cursor()
        sql = "DELETE FROM Reminder WHERE id = " + str(rowId)
        print("SQL: " + sql)
        cursor.execute(sql)
        connection.commit()
        connection.close()
        self.refreshData()        
        
    def due(self):
        today = time.strftime("%Y-%m-%d")
        return today in self.__appointmentDates
