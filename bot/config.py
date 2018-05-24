class Config(object):

    @staticmethod
    def validate_user_action(config:dict, step:str, user_response:dict):
        """Validate type of message
        Args:
            config (dict): configuration dict loads from global app settings
            message (string): message step - the next step of message that should be send
            user_response (dict): json response from vk server
        Returns:
            bool: True if message['type'] same as message type from config
            False if message['type'] is not valid"""
        for message in config['messages']:
            if message['key'] == step:
                for message_type in message['types']:
                    if not 'value' in message_type and \
                        message_type['type'] == user_response['type']:
                        return True
                    elif 'value' in message_type and \
                        message_type['type'] == user_response['type']:
                        """ TODO: rewrite for other types of messages """
                        print('here')
                        if user_response['object']['copy_history'][0]['id'] == \
                            message_type['value']:
                            return True
        return False

    @staticmethod
    def get_message_instance(messages:list, step:str):
        """Get message dict from config """
        for message in messages:
            if message['key'] == step:
                return message
                


