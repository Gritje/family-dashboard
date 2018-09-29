import kivy
import os
import random

from pygame import mixer

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button

class PictureFrame(BoxLayout):
    
    def __init__(self, **kwargs):
        super(PictureFrame, self).__init__(**kwargs)

        self.image = Image(source = self.__getRandomPicture(), allow_stretch=True)
        self.add_widget(self.image)
         
    def __getRandomPicture(self):
        pictures = os.listdir('pics/frame')
        r = random.randint(0,len(pictures)-1)
        return 'pics/frame/' + pictures[r]    
        
    def updateRandomPicture(self):
        self.image.source = self.__getRandomPicture()
        self.image.reload()
