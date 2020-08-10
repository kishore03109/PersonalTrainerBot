class UserData:
    def __init__(self, user_id, tz, weights, exercise, reminder):
        self.user_id = user_id
        self.tz = tz
        self.weights = weights
        self.exercise = exercise
        self.reminder = reminder

    def __repr__(self):
        return '{user_id:' + self.user_id \
                + ', tz:'+str(self.tz) + '}'
