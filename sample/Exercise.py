from datetime import datetime


class Exercise:
    def __init__(self, tz=None):
        self.datetime = datetime.now(tz).strftime('%D')

    def __repr__(self):
        return '{datetime:'+str(self.datetime) + '}'

