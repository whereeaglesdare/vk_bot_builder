class Validator(object):
    """ Defines pattern or types for incoming messages """
    def __init__(self, message: str, validator: str):
        self.message = message 
        self.validator = getattr(Validator, validator)

    @staticmethod
    def digit(message):
        return message.isdigit()


    @staticmethod
    def vk_user(message):
        if 'vk.com/' in message:
            return True
        else:
            return False

    def validate(self):
        if self.validator(self.message):
            return True
        else:
            return False

if __name__ == "__main__":
    validator = Validator("1", "digit").validate()
    print(validator)