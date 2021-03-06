import time
import kivy

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class Schedule(BoxLayout):
    
    def __init__(self, **kwargs):
        super(Schedule, self).__init__(**kwargs)
        
        self.orientation = 'vertical'
        self.scheduleTable = ScheduleTable()
        self.add_widget(self.scheduleTable)
    
    def __isWeekend(self):
        weekday = time.strftime("%w") # 0 = Sunday
        return weekday == "0" or weekday == "6"
    
    def __hideScheduleTable(self, hide):
        if hide:
            self.scheduleTable.opacity = 0.1
        else:
            self.scheduleTable.opacity = 1
            
    def handleScheduleDisplay(self):
        self.__hideScheduleTable(self.__isWeekend())
            
    
class ScheduleTable(GridLayout):
    
    def __init__(self, **kwargs):
        super(ScheduleTable, self).__init__(**kwargs)
        
        self.cols = 6
        self.row_force_default = True
        self.row_default_height = 40
        
        self.add_widget(Label(text= '[b]Zeit[/b]', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='[color=#ff4d4d][b]Montag[/b][/color]', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='[color=#ff9933][b]Dienstag[/b][/color]', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='[color=#ffff00][b]Mittwoch[/b][/color]', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='[color=#33cc33][b]Donnerstag[/b][/color]', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='[color=#ff6699][b]Freitag[/b][/color]', size_hint_x=None, width=100, markup = True))
        
        self.add_widget(Label(text='07:55', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Mathe', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Lesen', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Mathe', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Deutsch', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Mathe', size_hint_x=None, width=100, markup = True))

        self.add_widget(Label(text='08:45', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Deutsch', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Sport', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Religion', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='HWSU', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Deutsch', size_hint_x=None, width=100, markup = True))

        self.add_widget(Label(text='10:05', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Deutsch', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Deutsch', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Deutsch', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Mathe', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Musik', size_hint_x=None, width=100, markup = True))

        self.add_widget(Label(text='10:55', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Kunst', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='HWSU', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Sport', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Kunst', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Klassenrat', size_hint_x=None, width=100, markup = True))

        self.add_widget(Label(text='12:00', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Mathe', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Kunst', size_hint_x=None, width=100, markup = True))

        self.add_widget(Label(text='Betreuung', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Basteln\n(14:00-15:00)', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='Basketball\n(14:00-15:30)', size_hint_x=None, width=100, markup = True))
        self.add_widget(Label(text='', size_hint_x=None, width=100, markup = True))
