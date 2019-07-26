import time
import kivy
import sqlite3

from functools import partial

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.button import Button
from kivy.uix.image import Image


class PersonPopup(Popup):

    def __init__(self, root, **kwargs):
        super(PersonPopup, self).__init__(**kwargs)
        
        self._popupLayout = BoxLayout(orientation = 'vertical', spacing = 10)
        
        self._root = root
        self.stars = 0
        
        self._memberLayout = BoxLayout(orientation='horizontal')       
        self._memberLayout.add_widget(self._createMemberButton('Papa'))
        self._memberLayout.add_widget(self._createMemberButton('Mama'))
        self._memberLayout.add_widget(self._createMemberButton('Fiete'))
        self._memberLayout.add_widget(self._createMemberButton('Oma'))
        
        self._cancelButton = Button(text='Abbrechen')        
        self._cancelButton.bind(on_press=self.dismiss)
        
        self._popupLayout.add_widget(self._memberLayout)
        self._popupLayout.add_widget(self._cancelButton)
       
        self.title = 'Wer hat die Aufgabe erledigt?'
        self.content = self._popupLayout
        self.auto_dismiss = False
        
    def _createMemberButton(self, name):
        memberButton = ToggleButton(text=name, group='members', state='normal')
        memberButton.bind(on_press=self._doneCallback)
        return memberButton
        
    def _doneCallback(self, *args):
        
        connection = sqlite3.connect("dashboard.db")
        cursor = connection.cursor()
       
        member = ''
        
        memberButtons = ToggleButtonBehavior.get_widgets('members')
        for m in memberButtons:
            if m.state == 'down':
                member = m.text
                break
            
        sql = "UPDATE stars SET stars=(SELECT stars FROM stars WHERE member='" + member + "') + " + str(self.stars) + " WHERE member = '" + member + "'"
        print("SQL: " + sql)
        cursor.execute(sql)
        connection.commit()
        connection.close()
        
        self._root.refreshData()
        self.dismiss()

class TodoList(GridLayout):
    
    def __init__(self, **kwargs):
        super(TodoList, self).__init__(**kwargs)
        
        self.cols = 3
        self.row_force_default = True
        self.row_default_height = 40
        
        self.personPopup = PersonPopup(self)
        
        self._addCheckBox('Staub wischen', 2)
        self._addCheckBox('Schuhe putzen', 3)
        self._addCheckBox('Biom'+unichr(252)+'ll entsorgen', 1)
        self._addCheckBox('Geschirrsp'+unichr(252)+'ler einr'+unichr(228)+'umen', 1)
        self._addCheckBox('Geschirrsp'+unichr(252)+'ler ausr'+unichr(228)+'umen', 1)
        self._addCheckBox('Tisch aufdecken', 1)
        self._addCheckBox('Tisch abdecken', 1)
        self._addCheckBox('Ausfegen', 2)
        self._addCheckBox('Zimmer aufr'+unichr(228)+'umen', 1)
        self._addCheckBox('W'+unichr(228)+'sche zusammenlegen', 2)
        self._addCheckBox('Frische Br'+unichr(246)+'tchen holen', 4)

        #self.starImage = Image(source='pics/star.png')
        #self.add_widget(self.starImage)
        self.statsLabel = Label(text= "Papa: 0 Mama: 0 Fiete: 0 Oma: 0", markup = True)
        self.add_widget(self.statsLabel)
        
        self.resetButton = Button(text='Zur'+unichr(252)+'cksetzen', size=(100, 30), size_hint=(None, None))        
        self.resetButton.bind(on_press=self._resetStats)
        self.add_widget(self.resetButton)
        
        self.refreshData()
        
    def _addCheckBox(self, title, stars):
        checkbox = CheckBox(color=[0,255,0,100])                      
        checkbox.bind(active=partial(self._on_checkbox_active, stars))
        self.add_widget(checkbox)
        self.add_widget(Label(text= '[b]' + title +'[/b]', markup = True, font_size='20sp'))
        
        starText = ''
        for i in range(stars):
            starText+= "* "
        self.add_widget(Label(text= '[b]'+ starText +'[/b]', markup = True))        
    

    def _on_checkbox_active(self, stars, checkbox, value):
        self.personPopup.stars = stars
        self.personPopup.open()        
        #if value:
        #    print('The checkbox', checkbox, 'is active')
        #else:
        #    print('The checkbox', checkbox, 'is inactive')

    def _resetStats(self, *args):
        connection = sqlite3.connect("dashboard.db")
        cursor = connection.cursor()
        sql = "UPDATE stars SET stars=0"
        print("SQL: " + sql)
        cursor.execute(sql)
        connection.commit()
        connection.close()        
        self.refreshData()
    
    def refreshData(self):
        #self.remove_widget(self.starImage)
        self.remove_widget(self.statsLabel)
        self.remove_widget(self.resetButton)
        
        connection = sqlite3.connect("dashboard.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM stars ORDER BY stars DESC")
        
        statsText = ""
        for row in cursor:
            member = str(row[0])
            stars = str(row[1])            
            statsText += '[b]' + member + '[/b]' + ": " + stars + "   "          

        connection.close()
        
        self.add_widget(self.resetButton)
        #self.add_widget(self.starImage)
        self.statsLabel.text = statsText
        self.add_widget(self.statsLabel)
        
        memberButtons = ToggleButtonBehavior.get_widgets('members')
        for m in memberButtons:
            m.state = 'normal'


      