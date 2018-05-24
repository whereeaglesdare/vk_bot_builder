# from bot import app

class Message(object):
    """ Creates Dynamically changed values in messages and send
    Args:
        token (str): community access token to make requests
        template (str): static text in message
    """
    def __init__(self, token:str, template, **kwargs):
        self.token = token
        self.template=template

    def send_message(self, template, words):
        print(template % words)

    def user_first_name_and_random_link(self, album):
        words = (album, '2', '3')
        self.send_message(self.template, words)

    def album_text_hanlder(self, album): 
        words=(album,)
        print(album)
        # words = (kwargs.get('upload_album', None), )
        self.send_message(self.template, words)
