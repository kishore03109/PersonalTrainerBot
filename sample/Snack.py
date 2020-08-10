from datetime import datetime

class Snack:
  def __init__(self, description, hunger_level, tz=None):
    self.description = description
    self.hunger_level = hunger_level
    self.datetime = datetime.now(tz).isoformat(' ').split(".",1)[0]

  def __repr__(self):
    return '{description:' + self.description \
    + ', hunger_level:' + str(self.hunger_level) \
    + ', datetime:'+str(self.datetime) + '}'

