import sqlite3
import time
from datetime import datetime
from datetime import timedelta
from datetime import date
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

class NewAppointmentPopup(Popup):
      
    def __init__(self, root, **kwargs):
        super(NewAppointmentPopup, self).__init__(**kwargs)
        
        self._root = root
        self._popupLayout = BoxLayout(orientation = 'vertical')
        
        self._datetimePicker = DatetimePicker()
        self._appointmentTitleInput = TextInput(text='Was?', multiline=False)
        self._memberLayout = BoxLayout(orientation='horizontal')       
        self._memberButton1 = ToggleButton(text='Papa', group='members', state='down')
        self._memberButton2 = ToggleButton(text='Mama', group='members')
        self._memberButton3 = ToggleButton(text='Fiete', group='members')
        self._memberButton4 = ToggleButton(text='Oma', group='members')
        self._memberLayout.add_widget(self._memberButton1)
        self._memberLayout.add_widget(self._memberButton2)
        self._memberLayout.add_widget(self._memberButton3)
        self._memberLayout.add_widget(self._memberButton4)      
        self._saveButton = Button(text='Speichern')
        
        self._popupLayout.add_widget(self._datetimePicker)
        self._popupLayout.add_widget(self._appointmentTitleInput)
        self._popupLayout.add_widget(self._memberLayout)
        self._popupLayout.add_widget(self._saveButton)
        
        self.title='Neuer Termin:'
        self.content=self._popupLayout
        self.auto_dismiss=False
        self.bind(on_dismiss=self._newAppointmentCallback)
        self._saveButton.bind(on_press=self.dismiss)
        
    def _newAppointmentCallback(self, *args):
        appointment = self._appointmentTitleInput.text
        appointmentTime = self._datetimePicker.get_datetime()
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
        self._root.refreshData()
        
class NewReminderPopup(Popup):

    def __init__(self, root, **kwargs):
        super(NewReminderPopup, self).__init__(**kwargs)
        
        self._popupLayout = BoxLayout(orientation = 'vertical')
        
        self._root = root
        
        self._starttimePicker = DatetimePicker()
        self._reminderTitleInput = TextInput(text='Was?', multiline=False)
        self._saveButton = Button(text='Speichern')
        self._interval = TextInput(text='1', multiline=False)
        self._popupLayout.add_widget(self._starttimePicker)
        self._popupLayout.add_widget(self._reminderTitleInput)
        self._popupLayout.add_widget(self._interval)
        self._popupLayout.add_widget(self._saveButton)
        
        self.title='Neue Erinnerung:'
        self.content=self._popupLayout
        self.auto_dismiss=False
        self.bind(on_dismiss=self._newReminderCallback)
        self._saveButton.bind(on_press=self.dismiss)
        
    def _newReminderCallback(self, *args):
        startTime = self._starttimePicker.get_datetime()
        reminder = self._reminderTitleInput.text
        intervalInWeeks = self._interval.text
        connection = sqlite3.connect("dashboard.db")
        cursor = connection.cursor()
        dateStr = str(startTime.strftime("%Y-%m-%d")) # 2018-05-15
        
        sql = "INSERT INTO Reminder(startdate, text, interval) VALUES(date('"+ dateStr +"'), '" + reminder + "', " + str(intervalInWeeks) + ")"
        print("SQL: " + sql)
        cursor.execute(sql)
        connection.commit()
        connection.close()
        self._root.refreshData()

class Appointments(BoxLayout):
    
    def __init__(self, **kwargs):
        super(Appointments, self).__init__(**kwargs)
        
        self.orientation='vertical'
        
        self.newAppointmentButton = Button(text='Neuer Termin...', size=(200, 50), size_hint=(None, None), font_size=14)
        self.newReminderButton = Button(text='Neue Erinnerung...', size=(200, 50), size_hint=(None, None), font_size=14)
                
        self.appointmentPopup = NewAppointmentPopup(self)
        self.newAppointmentButton.bind(on_press=self.appointmentPopup.open)
        self.add_widget(self.newAppointmentButton)
        
        self.reminderPopup = NewReminderPopup(self)
        self.newReminderButton.bind(on_press=self.reminderPopup.open)
        self.add_widget(self.newReminderButton)
        
        self.grid = GridLayout(cols = 4)
        self.grid.row_force_default=True
        self.grid.row_default_height=40
        self.add_widget(self.grid)
        self.__appointments = []
        self.__reminders = []
        self.refreshData()

    def refreshData(self):
        connection = sqlite3.connect("dashboard.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Appointment ORDER BY appdate DESC")

        self.__appointments = []

        self.remove_widget(self.grid)
        self.grid = GridLayout(cols = 4)
        self.grid.row_force_default=True
        self.grid.row_default_height=40
        self.add_widget(self.grid)        
        
        for row in cursor:
            date = str(row[1])
            time = str(row[2])
            title = str(row[3])
            member = str(row[4])
            self.__appointments.append(AppointmentData(date, time, title, member))
            self.grid.add_widget(Label(text= date + ' ' + time)) #date time
            self.grid.add_widget(Label(text= title)) #appointment          
            self.grid.add_widget(Label(text= '[b][color=' + self.getColorForName(member) + ']' + member + '[/color][/b]', markup = True)) #family member
            deleteButton = Button(text='[color=#ff0000]X[/color]', size=(40, 40), size_hint=(None, None), markup = True)
            deleteButton.bind(on_press=partial(self.deleteAppointmentCallback, row[0])) #id 
            self.grid.add_widget(deleteButton)
            
        cursor.execute("SELECT * FROM Reminder ORDER BY startdate DESC")
        
        self.__reminders = []
        
        for row in cursor:
            startDate = str(row[1])
            text = str(row[2])
            intervalInWeeks = str(row[3])
            self.__reminders.append(ReminderData(startDate, text, intervalInWeeks))
            self.grid.add_widget(Label(text= startDate)) 
            self.grid.add_widget(Label(text= text))  
            self.grid.add_widget(Label(text= intervalInWeeks + ' Woche(n)'))
            deleteReminderButton = Button(text='[color=#ff0000]X[/color]', size=(40, 40), size_hint=(None, None), markup = True)
            deleteReminderButton.bind(on_press=partial(self.deleteReminderCallback, row[0])) #id 
            self.grid.add_widget(deleteReminderButton)            
            
        connection.close()
     
    def getColorForName(self, name):
        nameToColorMap = {'Papa': '#00ffff', 'Mama': '#ff6699', 'Oma': '#ffff00', 'Fiete': '#33cc33'}
        return nameToColorMap.get(name)                

    def deleteAppointmentCallback(self, rowId, *args):
        connection = sqlite3.connect("dashboard.db")
        cursor = connection.cursor()
        sql = "DELETE FROM Appointment WHERE id = " + str(rowId)
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
        appointmentsToday = []
        
        for a in self.__appointments:
            if today == a.date:
                appointmentsToday.append(a)
                
        return appointmentsToday
    
    def remind(self):
        today = datetime.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d")        
        remindersToday = []
        
        for r in self.__reminders:
            reminderStart = datetime.strptime(r.startDate, "%Y-%m-%d")
            while reminderStart <= today:
                if today == reminderStart:
                    remindersToday.append(r)
                reminderStart = reminderStart + timedelta(days=7)                
                
        return remindersToday        
    
    
class AppointmentData():
    
    def __init__(self, date, time, title, member):
    
        self.date = date
        self.time = time
        self.datetime = date + ' ' + time
        self.title = title
        self.member = member
        
class ReminderData():
    
    def __init__(self, startDate, text, intervalInWeeks):
    
        self.startDate = startDate
        self.text = text
        self.intervalInWeeks = intervalInWeeks        
    
