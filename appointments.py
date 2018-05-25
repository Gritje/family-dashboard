import sqlite3
import kivy

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.garden.datetimepicker import DatetimePicker
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown

from functools import partial

class Appointments(BoxLayout):
    
    def __init__(self, **kwargs):
        super(Appointments, self).__init__(**kwargs)

        self.orientation='vertical'
        
        self.newAppointmentButton = Button(text='Neuer Termin...', font_size=14)
        
        self.popupLayout = BoxLayout(orientation = 'vertical')        
        self.datetimePicker = DatetimePicker()
        self.appointmentTitleInput = TextInput(text='Neuer Termin', multiline=False)
        self.appointmentMemberSelection = MemberDropDown()
        self.saveButton = Button(text='Speichern')
        self.popupLayout.add_widget(self.datetimePicker)
        self.popupLayout.add_widget(self.appointmentTitleInput)
        #self.popupLayout.add_widget(self.appointmentMemberSelection)
        self.popupLayout.add_widget(self.saveButton)
        self.popup = Popup(title='Neuer Termin', content=self.popupLayout, auto_dismiss=False)
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
        
        
class MemberDropDown(DropDown):
        
    def __init__(self, **kwargs):
        super(MemberDropDown, self).__init__(**kwargs)

        btn0 = Button(text='Fiete', size_hint_y=None, height=44)
        # attach a callback that will call the select() method
        # pass the text of the button as the data of the selection
        btn0.bind(on_release=lambda btn0: self.select(btn0.text))
        self.add_widget(btn0)

        btn1 = Button(text='Mama', size_hint_y=None, height=44)
        btn1.bind(on_release=lambda btn1: self.select(btn1.text))
        self.add_widget(btn1)
        
        btn2 = Button(text='Papa', size_hint_y=None, height=44)
        btn2.bind(on_release=lambda btn2: self.select(btn2.text))
        self.add_widget(btn2)
        
        btn3 = Button(text='Oma', size_hint_y=None, height=44)
        btn3.bind(on_release=lambda btn3: self.select(btn3.text))
        self.add_widget(btn3)

        self.mainbutton = Button(text='Fiete', size_hint=(None, None))

        # show the dropdown menu when the main button is released
        # note: all the bind() calls pass the instance of the caller (here, the
        # mainbutton instance) as the first argument of the callback (here,
        # dropdown.open.).
        self.mainbutton.bind(on_release=self.open)

        # isten for the selection in the dropdown list and assign the data to the button text
        self.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
