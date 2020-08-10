from datetime import datetime


class Weight:
    def __init__(self, value, tz=None):
        self.value = value
        self.datetime = datetime.now(tz).strftime('%D')

    def __repr__(self):
        return '{value:' + self.value \
                + ', datetime:'+str(self.datetime) + '}'

