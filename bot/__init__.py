from flask import Flask

app = Flask(__name__)

from bot import routes, message_handler, messages, utils, config

app.config['microservice_config'] = config.FileBotConfig('config.json').load()