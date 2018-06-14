class Validator(object):
    """ Defines pattern or types for incoming messages """
    def __init__(self, message: str, validator: str):
        self.message = message 
        self.validator = getattr(Validator, validator)

    @staticmethod
    def digit(message):
        return message.isdigit()

    def validate(self):
        if self.validator(self.message):
            return True
        else:
            return False
