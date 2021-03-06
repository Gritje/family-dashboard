import kivy
import time

from ledmatrix import LedMatrix

from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
from kivy.core.window import Window
from kivy.clock import Clock

from kivy.app import App
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.button import Button

from overview import Overview
from feeds import Feeds
from appointments import Appointments
from schedule import Schedule
from todoList import TodoList
from pictureFrame import PictureFrame

class DashboardApp(App):
    
    def build(self):
        self.root = Accordion(min_space=30)
        
        self.overviewItem = AccordionItem(title=unichr(252) + 'bersicht')
        self.overview = Overview()
        self.overviewItem.add_widget(self.overview)
        #self.closeButton = Button(text = 'Beenden', size=(100, 50), size_hint=(None, None), background_color=[1,0,0,1])
        #self.closeButton.bind(on_press=self.closeApp)
        #self.overviewItem.add_widget(self.closeButton)
        self.root.add_widget(self.overviewItem)
      
        self.scheduleItem = AccordionItem(title='Stundenplan')
        self.schedule = Schedule()
        self.scheduleItem.add_widget(self.schedule)
        self.root.add_widget(self.scheduleItem)
        
        self.appointmentsItem = AccordionItem(title='Termine')
        self.appointments = Appointments()
        self.appointmentsItem.add_widget(self.appointments)
        self.root.add_widget(self.appointmentsItem)
        
        self.todoListItem = AccordionItem(title='Haushalts-Abenteuer')
        self.todoList = TodoList()
        self.todoListItem.add_widget(self.todoList)
        self.root.add_widget(self.todoListItem)

        self.newsItem = AccordionItem(title='Nachrichten')
        self.news = Feeds()
        self.newsItem.add_widget(self.news)
        self.root.add_widget(self.newsItem)

        self.pictureItem = AccordionItem(title='Bilder')
        self.pictureFrame = PictureFrame()
        self.pictureItem.add_widget(self.pictureFrame)    
        self.root.add_widget(self.pictureItem)
        
        self.scheduleItem.collapse = False
        
        self.ledClock = LedMatrix()

        # initial weather data
        self.overview.updateWeather()
        # continuous updates
        EACH_SECOND = 1
        ONE_MINUTE = 60
        FOUR_HOURS = 14400
        Clock.schedule_interval(self.__updateLedClock, EACH_SECOND)
        Clock.schedule_interval(self.__updateItems, ONE_MINUTE)
        Clock.schedule_interval(self.__updateWeather, FOUR_HOURS)
        
        return self.root
    
    def __updateWeather(self, dt):
        self.overview.updateWeather()
               
    def __updateLedClock(self, dt):
        self.ledClock.updateLedDisplay(time.strftime("%H:%M:%S"))
        
    def __updateItems(self, dt):
        self.overview.updateDateTime()        
        self.news.refreshFeeds()
        self.pictureFrame.updateRandomPicture()
        self.schedule.handleScheduleDisplay()
        dueAppointments = self.appointments.due()
        if not dueAppointments:
            self.appointmentsItem.title = 'Termine'
        else:
            self.appointmentsItem.title = 'Termin(e) >>heute<<'
            self.overview.updateAppointmentTile(dueAppointments)
            
        dueReminders = self.appointments.remind()
        if dueReminders:
            self.overview.updateReminderTile(dueReminders)    
        
    def closeApp(self, instance):
        self.stop()

if __name__ == '__main__':
    DashboardApp().run()
