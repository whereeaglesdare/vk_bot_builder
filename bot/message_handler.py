import random

import redis
from bot.utils import Config
from bot.messages import Message


class MessageHandler(object):
    def __init__(self, config, response):
        self.user_id = response['object']['user_id'] if  response['object'].get('user_id', None) \
            is not None else  response['object']['from_id']
        self._step = None
        self.redis_connection = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.config = config
        self.user_response = response

    def get_step(self):
        self._step = self.redis_connection.get(self.user_id)
        return self._step.decode() if self._step is not None else None

    def set_step(self, next_step):
        self.redis_connection.set(self.user_id, next_step)

    def get_token(self):
        return random.choice(self.config['community_tokens'])

    def make_response(self):
        if not self.get_step() and Config.validate_user_action(self.config, self.config['start_message'],
                                                               self.user_response):
            next_message = Config.get_message_instance(messages=self.config['messages'],
                                                       step=self.config['start_message'])
        else:
            step = self.get_step()
            message = Config.get_message_instance(messages=self.config['messages'], step=step)
            if self.user_response['type'] != 'message_new':
                return 
            redirect = Config.check_keyword(message, self.user_response)
            if redirect is not None:
                next_message = Config.get_message_instance(messages=self.config['messages'], step=redirect)
            else:
                next_message = Config.get_message_instance(messages=self.config['messages'],
                                                           step=message['error_redirect'])
        _message_instance = Message(token=self.get_token(), user_id=self.user_id, template=next_message['message'],
                                    redis_connection=self.redis_connection)
        Config.get_handler_requirements(next_message, self.config)
        getattr(_message_instance, next_message['handler'])(**Config.get_handler_requirements(next_message,
                                                                                              self.config))
        self.set_step(next_message['key'])

