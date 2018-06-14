import datetime

import vk_api
import requests

class Message(object):
    """ Creates Dynamically changed values in messages and send
    Args:
        token (str): community access token to make requests
        template (str): static text in message
    """
    def __init__(self, token:str, template:str, user_id:int, 
                 redis_connection, user_response:dict, handler:str):
        self.vk = vk_api.VkApi(token=token).get_api()
        self.template = template
        self.redis_connection = redis_connection
        self.user_id = user_id
        self.user_response = user_response
        self.handler = getattr(handler, handler)

    def send_message(self, template, words):
        self.vk.messages.send(user_id=self.user_id, message=template % words)
        return template % words
        
    def user_first_name_and_random_link(self, **kwargs):
        random_id = "http://vk.com/id" + str(self.redis_connection.randomkey().decode())
        name = self.vk.users.get(user_ids=self.user_id, lang='ru_RU')[0]['first_name']
        words = (name, random_id, kwargs.get('upload_album', None))

        self.send_message(self.template, words)

    def album_text_hanlder(self, **kwargs): 
        words=(kwargs.get('upload_album', None),)
        self.send_message(self.template, words)

    def default_handler(self, **kwargs):
        self.send_message(self.template, ())

    def user_first_name_handler(self, **kwargs):
        words = (self.vk.users.get(user_ids=self.user_id, lang='ru_RU')[0]['first_name'], )
        self.send_message(self.template, words)

    def ban_handler(self, **kwargs):
        self.send_message(self.template, ())
        editor_token = kwargs.get('editor_token', None)
        group_id = kwargs.get('group_id', None)
        ban_reason = kwargs.get('ban_reason', None)
        user_session =  vk_api.VkApi(token=editor_token).get_api()
        ts = int(datetime.datetime.now().timestamp()) + 24 * 3600
        user_session.groups.ban(group_id=group_id, owner_id=self.user_id,
                                reason=4, comment=ban_reason, end_date=ts)
    
    def redirect_handler(self, **kwargs):
        r = requests.post(url=kwargs.get('redirect_url'), json=self.user_response)

    def unpack(self, args):
        if self.handler(args):
            return True
        else:
            return False