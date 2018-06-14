import random

import redis
from bot.manager import Manager
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
        step = self.get_step()
        manager = Manager(config=self.config, user_response=self.user_response, step=step)
        if not step and manager.validate_user_action(self.config['start_message']):
            next_message = manager.get_message_instance(step=self.config['start_message'])
        else:
            if self.user_response['type'] != 'message_new':
                return 
            redirect = manager.get_redirect()
            next_message = manager.get_message_instance(step=redirect)
        message = Message(token=self.get_token(), user_response=self.user_response, 
                          template=next_message['message'],
                          redis_connection=self.redis_connection, user_id=self.user_id, 
                          handler=manager.get_message_instance()['handler'])
        message.unpack(manager.get_handler_requirements(next_message))
        self.set_step(redirect)

if __name__ == "__main__":
    with open('../config.json') as f:
        data = json.load(f)
        #response = {"type":"wall_repost","object":{"id":67,"from_id":366467480,"owner_id":324993092,"date":1527151487,"post_type":"post","text":"","copy_history":[{"id":194,"owner_id":-162833914,"from_id":-162833914,"date":1527149366,"post_type":"post","text":"эту запись должны репостить","post_source":{"type":"vk"}}],"comments":{"count":0}},"group_id":162833914}
        response = {"type":"message_new","object":{"id":2945,"date":1527159975,"out":0,"user_id":324993092,"read_state":0,"title":"","body":"as"},"group_id":162833914}
        m = MessageHandler(config=data, response=response)
        m.make_response()
