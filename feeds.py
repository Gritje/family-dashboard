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
        self.feeds()

    def feeds(self):
        trainFeed = feedparser.parse('https://www.deutschebahn.com/service/rss/pr-hamburg-de/1309346/feed.rss')     
        sponFeed = feedparser.parse('http://www.spiegel.de/schlagzeilen/tops/index.rss')
     
        self.add_widget(Label(text = '[b][color=#00ffff]Nachrichten[/color][/b]', size=(600, 40), size_hint=(None, None), font_size='32sp', markup = True))

        # SPON feeds
        spinnerList = []
        for post in sponFeed.entries:
             spinnerList.append(post.title)
             
        sponSpinner = Spinner(text=sponFeed.entries[0].title, values=spinnerList)
        sponDescriptionLabel = Label(text = sponFeed.entries[0].description, size=(600, 100), size_hint=(None, None), halign = 'left', valign = 'middle')
        sponDescriptionLabel.text_size = sponDescriptionLabel.size

        def getDescription(text):
            description = ''
            for post in sponFeed.entries:
                if post.title == text:
                    return post.description
            return description

        def show_selected_value(sponSpinner, text):
            sponDescriptionLabel.text = getDescription(text)

        sponSpinner.bind(text=show_selected_value)
          
        self.add_widget(sponSpinner)
        self.add_widget(sponDescriptionLabel)

        # Train feeds    
        self.add_widget(Label(text = '[b][color=#00ffff]Bahn[/color][/b]', size=(600, 40), size_hint=(None, None), font_size='32sp', markup = True))
     
        spinnerList = []
        for post in trainFeed.entries:
            spinnerList.append(post.title)

        trainSpinner = Spinner(text=trainFeed.entries[0].title, values=spinnerList)
        trainDescriptionLabel = Label(text = trainFeed.entries[0].description, size=(600, 100), size_hint=(None, None), halign = 'left', valign = 'middle')
        trainDescriptionLabel.text_size = trainDescriptionLabel.size

        def getTrainDescription(text):
            description = ''
            for post in trainFeed.entries:
                if post.title == text:
                    return post.description
            return description

        def show_selected_value2(trainSpinner, text):
            trainDescriptionLabel.text = getTrainDescription(text)

        trainSpinner.bind(text=show_selected_value2)

        self.add_widget(trainSpinner)
        self.add_widget(trainDescriptionLabel)
    