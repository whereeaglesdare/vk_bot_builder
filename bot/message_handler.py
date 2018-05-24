import json

import redis
from config import Config
from messages import Message


class MessageHandler(object):
    def __init__(self, user_id, config, response):
        self.user_id = user_id
        self._step = None
        self.redis_connection = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.config = config
        self.user_response = response

    def get_step(self):
        self._step = self.redis_connection.get(self.user_id)

        return self._step.decode() if self._step is not None else None

    def set_step(self, next_step):
        self.redis_connection.set(self.user_id, next_step)


    def make_response(self):
        if not self.get_step() and Config.validate_user_action(self.config, self.config['start_message'], \
                self.user_response):
            self.set_step(self.config['start_message'])
            message = Config.get_message_instance(messages=self.config['messages'], step=self.config['start_message'])
            m = Message(token='123', template=message['message'])
            if message.get('requires', None) is not None:
                print(message['requires'], self.config[message['requires']], 'here')
                values = getattr(m, message['handler'])(self.config[message['requires']])
            else:
                values = getattr(m, step['handler'])() 
        else:
            step = self.get_step()
            message = Config.get_message_instance(messages=self.config['messages'], step=step)
            for keyword in message['accept_keyword']: 
                if self.user_response['object']['body'].lower() == keyword['keyword'].lower():
                    step = keyword['redirect']
                    next_message_instance = Config.get_message_instance(messages=self.config['messages'], step=step)
                    m = Message(token='123', template=next_message_instance['message'])
                    if next_message_instance.get('requires', None) is not None:
                        values = getattr(m, next_message_instance['handler'])(self.config[next_message_instance['requires']])
                    else:
                        values = getattr(m, next_message_instance['handler'])()
                    self.set_step(step)
                    return values


if __name__ == "__main__":
    with open('../config.json') as f:
        data = json.load(f)
        # response = {"type":"wall_repost","object":{"id":67,"from_id":366467480,"owner_id":366467480,"date":1527151487,"post_type":"post","text":"","copy_history":[{"id":194,"owner_id":-162833914,"from_id":-162833914,"date":1527149366,"post_type":"post","text":"эту запись должны репостить","post_source":{"type":"vk"}}],"comments":{"count":0}},"group_id":162833914}
        response = {"type":"message_new","object":{"id":2945,"date":1527159975,"out":0,"user_id":366467480,"read_state":0,"title":"","body":"правила"},"group_id":162833914}
        m = MessageHandler(user_id=366467480, config=data, response=response)
        m.make_response()