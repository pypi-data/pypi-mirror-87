class PresentationSettings():

    def __init__(self, settings:dict = {}):
        self.title = settings['title'] if 'title' in settings else 'Presentation'
        self.theme = settings['theme'] if 'theme' in settings else 'black'
