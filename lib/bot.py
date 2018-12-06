from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from lib import loader
from lib.messages import log


class Bot:
    def __init__(self):
        # Define Base Variables
        self.CONFIG = loader.config()
        try:
            if self.CONFIG.get('PROXY_ON',False):
                self.updater = Updater(
                    token=self.CONFIG.get('TOKEN'),
                    request_kwargs={
                        'proxy_url': self.CONFIG.get('PROXY_URL', 'http://localhost:8123')
                    }
                )
            else:
                self.updater = Updater(token=self.CONFIG.get('TOKEN'))

            self.dispatcher = self.updater.dispatcher
        except Exception as e:
            log.error(__file__,'__init__',e)

    def start(self,webhook = loader.config().get('WEB_HOOK_ON',False)):
        try:
            if webhook:
                # Run Bot as webhook
                self.updater.start_webhook(
                    listen=self.CONFIG.get('WEB_HOOK_LISTEN','0.0.0.0'),
                    port=self.CONFIG.get('WEB_HOOK_PORT','8443'),
                    url_path=self.CONFIG.get('TOKEN')
                )
                self.updater.bot.set_webhook('{}{}'.format(self.CONFIG.get('WEB_HOOK_ADDRESS','localhost'), self.CONFIG.get('TOKEN')))
                self.updater.idle()
            else:
                self.updater.start_polling()
            log.info("Bot Started...")
        except Exception as e:
            log.error(__file__,'start',e)

    def addHandler(self,handler,filter,function):
        try:
            self.dispatcher.add_handler(handler(filter, function))
        except Exception as e:
            log.error(__file__,'addHandler',e)