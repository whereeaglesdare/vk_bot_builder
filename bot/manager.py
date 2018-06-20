from bot.validator import Validator

class Manager(object):
    def __init__(self, config:dict, user_response:dict, step:str):  
        """Validate type of message
        Args:
            config (dict): configuration dict loads from global app settings
            step (string): message step - the next step of message that should be send
            user_response (dict): json response from vk server
        """    
        self.config = config
        self.user_response = user_response
        self.step = step

    def validate_user_action(self, step=None) -> bool:
        """Method for checking incoming user action
        
        User action contains wall_repost, new_message or another 
        allowed action from Callback API settings
        Return:
            False if message['type'] is not valid
        """
        if step is None:
            step = self.step
        message = self.get_message_instance(step)
        for message_type in message['types']:
            if not 'value' in message_type and \
                message_type['type'] == self.user_response['type']:
                return True
            elif 'value' in message_type and \
                message_type['type'] == self.user_response['type']:
                """ TODO: rewrite for other types of messages """
                if self.user_response['object']['copy_history'][0]['id'] == \
                    message_type['value']:
                    return True
        return False

    def get_message_instance(self,  step=None):
        """Get message dict from config """
        if step is None:
            step = self.step
        for message in self.config['messages']:
            if message['key'] == step:
                return message
    
    def get_handler_requirements(self, message:dict):
        """ Get 'requires' key from message """
        requires_list = message.get('requires', None)
        if requires_list is None:
            return {}
        else:
            return { key:self.config[key] for key in requires_list }
    
    def get_redirect(self, step=None):
        if step is None:
            step = self.step
        message = self.get_message_instance(step)
        user_text_body = self.user_response['object']['body'].lower()
        for keyword in message['accept_keyword']:    
            if 'type' in keyword:
                if Validator(message=user_text_body, validator=keyword['type']).validate():
                    return keyword['redirect']
                else:
                    continue
            elif user_text_body == keyword['keyword'].lower():
                return keyword['redirect']
        return message['error_redirect']
