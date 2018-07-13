import kivy

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
from pictureFrame import PictureFrame

class DashboardApp(App):
    
    def build(self):
        self.root = Accordion()
        
        self.overviewItem = AccordionItem(title='Uebersicht')
        self.overview = Overview()
        self.overviewItem.add_widget(self.overview)
        self.root.add_widget(self.overviewItem)
      
        self.scheduleItem = AccordionItem(title='Stundenplan')
        self.schedule = Schedule()
        self.scheduleItem.add_widget(self.schedule)
        self.root.add_widget(self.scheduleItem)
        
        self.appointmentsItem = AccordionItem(title='Termine')
        self.appointments = Appointments()
        self.appointmentsItem.add_widget(self.appointments)
        self.root.add_widget(self.appointmentsItem)

        self.newsItem = AccordionItem(title='Nachrichten')
        self.newsItem.add_widget(Feeds())
        self.root.add_widget(self.newsItem)

        self.pictureItem = AccordionItem(title='Bilder')
        self.pictureItem.add_widget(PictureFrame())
        
        self.closeButton = Button(text = 'Beenden', size=(100, 50), size_hint=(None, None), background_color=[1,0,0,1])
        self.closeButton.bind(on_press=self.closeApp)
        self.pictureItem.add_widget(self.closeButton)
        self.root.add_widget(self.pictureItem)
        
        self.scheduleItem.collapse = False
        
        Clock.schedule_interval(self.__updateItems, 60)
        
        return self.root
    
    def __updateItems(self, dt):
        self.overview.updateDateTime()
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
