import feedparser
import kivy

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner

class Feeds(BoxLayout):
    
    def __init__(self, **kwargs):
        super(Feeds, self).__init__(**kwargs)

        self.orientation='vertical'
        self.spacing=10
        
        self.refreshFeeds()     
        
    def refreshFeeds(self):
        self.clear_widgets()
        self.sponFeed = feedparser.parse('http://www.spiegel.de/schlagzeilen/tops/index.rss')
        self.trainFeed = feedparser.parse('https://www.deutschebahn.com/service/rss/pr-hamburg-de/1309346/feed.rss')
        self.__feeds(self.sponFeed, 'Nachrichten')        
        self.__feeds(self.trainFeed, 'Bahn')        
    
    def __feeds(self, feed, headline):
        
        self.add_widget(Label(text = '[b][color=#00ffff]' + headline + '[/color][/b]', size=(600, 40), size_hint=(None, None), font_size='32sp', markup = True))
        
        if not feed.entries:
            self.add_widget(Label(text = 'Keine Internetverbindung - Daten koennen nicht abgerufen werden'))
        else:
        
            spinnerList = []
            for post in feed.entries:
                spinnerList.append(post.title)

            feedDescriptionLabel = Label(text = feed.entries[0].description, size=(600, 100), size_hint=(None, None), halign = 'left', valign = 'middle')
            feedDescriptionLabel.text_size = feedDescriptionLabel.size
            
            feedSpinner = Spinner(text=feed.entries[0].title, values=spinnerList)
            
            def show_selected_value(feedSpinner, text):
                feedDescriptionLabel.text = self.__getFeedDescription(feed, text)
                
            feedSpinner.bind(text=show_selected_value)

            self.add_widget(feedSpinner)
            self.add_widget(feedDescriptionLabel)
        
    def __getFeedDescription(self, feed, text):
        description = ''
        for post in feed.entries:
            if post.title == text:
                return post.description
        return description

     
