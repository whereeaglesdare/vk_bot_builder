import datetime
import json

import vk_api
import requests


class Message(object):
    """ Creates Dynamically changed values in messages and send
    Args:
        token (str): community access token to make requests
        template (str): static text in message
    """
    def __init__(self, token:str, template:str, user_id:int, 
                 redis_connection, user_response:dict, handler:str,
                 keyboard:dict):
        self.vk = vk_api.VkApi(token=token, api_version='5.80').get_api()
        self.template = template
        self.token = token
        self.redis_connection = redis_connection
        self.user_id = user_id
        self.user_response = user_response
        self.keyboard = keyboard if keyboard != {} else None
        self.handler = getattr(Message, handler)
        self.version = '5.80'

    def send_message(self, message):
        params = {
                'user_id': self.user_id,
                'access_token': self.token,
                'version': self.version,
                'message': message
        }
        if self.keyboard is not None:
            params['keyboard'] = json.dumps(self.keyboard, ensure_ascii=False)
        request = requests.post('https://api.vk.com/method/messages.send?', params=params)
        print(request.text, flush=True)

    def user_first_name_and_random_link(self, **kwargs):
        random_id = "http://vk.com/id" + str(self.redis_connection.randomkey().decode())
        name = self.vk.users.get(user_ids=self.user_id, lang='ru_RU')[0]['first_name']
        words = (name, random_id, kwargs.get('upload_album', None))
        self.send_message(message=self.template % words)

    def album_text_hanlder(self, **kwargs):
        words=(kwargs.get('upload_album', ''),)
        self.send_message(message=self.template % words)

    def default_handler(self, **kwargs):
        self.send_message(message=self.template)

    def user_first_name_handler(self, **kwargs):
        words = (self.vk.users.get(user_ids=self.user_id, lang='ru_RU')[0]['first_name'], )
        self.send_message(message=self.template % words)

    def ban_handler(self, **kwargs):
        self.send_message(self.template)
        editor_token = kwargs.get('editor_token', None)
        group_id = kwargs.get('group_id', None)
        ban_reason = kwargs.get('ban_reason', None)
        user_session =  vk_api.VkApi(token=editor_token).get_api()
        ts = int(datetime.datetime.now().timestamp()) + 24 * 3600
        user_session.groups.ban(group_id=group_id, owner_id=self.user_id,
                                reason=4, comment=ban_reason, end_date=ts)
    
    def redirect_handler(self, **kwargs):
        """Redirect text for old Callback API versions"""
        text = self.user_response['object']['text']
        message = {"type":"message_new","object":{"id":46428191,"date":1529507989,"out":0,"user_id":self.user_id,
                                                  "read_state":0,"title":"","body":text},"group_id":58526040}

        requests.post(url=kwargs.get('redirect_url'), json=message)

    def redirect_handler_with_template(self, **kwargs):
        """ Redirect with template message to old Callback API"""
        message = {"type":"message_new","object":{"id":46428191,"date":1529507989,"out":0,"user_id":self.user_id,
                                                  "read_state":0,"title":"","body":self.template},"group_id":58526040}
        self.user_response['object']['body'] = self.template
        r = requests.post(url=kwargs.get('redirect_url'), json=message)

    def unpack(self, args):
        if self.handler(self, **args):
            return True
        else:
            return False

