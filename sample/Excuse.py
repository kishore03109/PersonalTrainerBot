from datetime import datetime


class Excuse:
    def __init__(self, text, tz=None):
        self.text = text
        self.datetime = datetime.now(tz).strftime('%D')

    def __repr__(self):
        return '{text:' + self.text \
                + ', datetime:'+str(self.datetime) + '}'

