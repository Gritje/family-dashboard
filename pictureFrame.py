import kivy

from pygame import mixer

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button

class PictureFrame(BoxLayout):
    
    def __init__(self, **kwargs):
        super(PictureFrame, self).__init__(**kwargs)

        self.add_widget(Image(source='pics/sommer.jpg'))
        #btn = Button(text='Coin')
        #btn.bind(on_press=self.__makeSound)
        #self.add_widget(btn)
        
    #def __makeSound(self, instance):
    #    mixer.init()
    #    mixer.music.load('Mario-coin-sound.mp3')
    #    mixer.music.play()