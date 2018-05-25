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
                    print(message_type)
                    if not 'value' in message_type and \
                        message_type['type'] == user_response['type']:
                        return True
                    elif 'value' in message_type and \
                        message_type['type'] == user_response['type']:
                        """ TODO: rewrite for other types of messages """
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
                
    @staticmethod
    def get_handler_requirements(message:dict, config:dict):
        """ Get 'requires' key from message """
        requires_list = message.get('requires', None)
        if requires_list is None:
            return {}
        else:
            return { key:config[key] for key in requires_list }
    
    @staticmethod
    def check_keyword(message: dict, user_response:str):
        for keyword in message['accept_keyword']:
                if user_response['object']['body'].lower() == keyword['keyword'].lower():
                    return keyword['redirect']



