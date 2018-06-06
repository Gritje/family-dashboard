import kivy

from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
from kivy.core.window import Window

from kivy.app import App
from kivy.uix.accordion import Accordion, AccordionItem

from feeds import Feeds
from appointments import Appointments
from schedule import Schedule
from pictureFrame import PictureFrame

class DashboardApp(App):
    def build(self):
        root = Accordion()    
      
        scheduleItem = AccordionItem(title='Stundenplan')
        scheduleItem.add_widget(Schedule())
        root.add_widget(scheduleItem)
        
        appointmentsItem = AccordionItem(title='Termine')
        appointmentsItem.add_widget(Appointments())
        root.add_widget(appointmentsItem)

        newsItem = AccordionItem(title='Nachrichten')
        newsItem.add_widget(Feeds())
        root.add_widget(newsItem)

        pictureItem = AccordionItem(title='Bilder')
        pictureItem.add_widget(PictureFrame())
        root.add_widget(pictureItem)
        
        scheduleItem.collapse = False
        
        return root

if __name__ == '__main__':
    DashboardApp().run()
