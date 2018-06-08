import kivy

from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
from kivy.core.window import Window
from kivy.clock import Clock

from kivy.app import App
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.button import Button

from feeds import Feeds
from appointments import Appointments
from schedule import Schedule
from pictureFrame import PictureFrame

class DashboardApp(App):
    
    def build(self):
        self.root = Accordion()    
      
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
        
        self.closeButton = Button(text = 'Beenden')
        self.closeButton.bind(on_press=self.closeApp)
        self.pictureItem.add_widget(self.closeButton)
        self.root.add_widget(self.pictureItem)
        
        self.scheduleItem.collapse = False
        
        Clock.schedule_interval(self.__updateItems, 60)
        
        return self.root
    
    def __updateItems(self, dt):
        self.schedule.updateDateTime()
        if self.appointments.due():
            self.appointmentsItem.title = 'Termin >>>heute<<<'
        else:
            self.appointmentsItem.title = 'Termine'
        
    def closeApp(self, instance):
        self.stop()

if __name__ == '__main__':
    DashboardApp().run()
