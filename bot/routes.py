import json

from flask import request
from bot import app
from bot.message_handler import MessageHandler

@app.route('/', methods=['POST'])
def message_dispatcher():
    try:
        data = json.loads(request.data)
    except:
        app.logger.debug('Request with invalid data')
        return 'ok'
    if data['type'] == 'confirmation':
        app.logger.info('Confirm to server')
        return app.config['microservice_config']['confirmation_token']
    if 'secret' not in data or data['secret'] != app.config['microservice_config']['secret']:
        app.logger.critical('Request without secret key')
        return 'ok'
    MessageHandler(config=app.config['microservice_config'], response=data).make_response()
    return 'ok'

@app.route('/reconfigure', methods=['POST'])
def reconfigure():
    app.logger.debug('Bot reconfigure')
    return 'ok'