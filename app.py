import os
from telegram.ext import Updater

import bot_config
import commands

HOSTNAME = os.environ.get('WEBSITE_HOSTNAME')
URL_PATH = 'cnrail_query'

updater = Updater(token=bot_config.TG_TOKEN, use_context=True)


# add handlers to the commands.
for handler in commands.handlers:
    updater.dispatcher.add_handler(handler)


updater.start_webhook(
    listen='0.0.0.0',
    url_path=URL_PATH,
    webhook_url='https://' + HOSTNAME + '/' + URL_PATH,
    port=8000,
)

# TODO: check whether this is necessary
updater.idle()
