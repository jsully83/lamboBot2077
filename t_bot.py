from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from random import *
from datetime import datetime
from  urllib.parse import urljoin
from urllib.request import urlopen
from ccxt import bittrex
# import urlparse
import logging

import json
import pprint as pprint



GIPHY = "ecJmwzf6vdD8fozImQtiqElIUIpmd4wR"





class lamboBot2077(object):

    def __init__(self):
        self.bit = bittrex()

        self.updater = Updater(token='472894388:AAEjG7SEVkeJe2aihlnbyLD92cV-f4O5WQ0')
        self.handlers()


        self.bot = self.dispatcher.bot



        self.updater.start_polling()



        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)


    def handlers(self):
        # create dispatcher
        self.dispatcher = self.updater.dispatcher

        #create handler variables
        self.start_handler = CommandHandler('start', self.start)
        self.caps_handler = CommandHandler('caps', self.caps, pass_args=True)
        self.boom_handler = CommandHandler('boom', self.boom)
        self.lambos_handler = CommandHandler('lambos', self.lambos)
        self.help_handler = CommandHandler('help', self.help)
        self.gif_handler = CommandHandler('gif', self.gif, pass_args=True)
        self.ticker_handler = CommandHandler('t', self.ticker, pass_args=True)

        # self.echo_handler = MessageHandler(Filters.text, self.echo)
        self.unknown_handler = MessageHandler(Filters.command, self.unknown)

        # add to dispatcher
        self.dispatcher.add_handler(self.start_handler)
        # self.dispatcher.add_handler(self.echo_handler)
        self.dispatcher.add_handler(self.caps_handler)
        self.dispatcher.add_handler(self.boom_handler)
        self.dispatcher.add_handler(self.lambos_handler)
        self.dispatcher.add_handler(self.gif_handler)
        self.dispatcher.add_handler(self.help_handler)
        self.dispatcher.add_handler(self.ticker_handler)

        self.dispatcher.add_handler(self.unknown_handler)

    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Hi! I'm LamboBot2077. Type /help for help")

    # def echo(self, bot, update):
    #     bot.send_message(chat_id=update.message.chat_id, text="I was promised lambos Kevin!")

    def unknown(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="LamboBot2077 does not compute. No lambos for you!")

    def caps(self, bot, update, args):
        text_caps = ' '.join(args).upper()
        bot.send_message(chat_id=update.message.chat_id, text=text_caps)

    def boom(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Boom!")

    def lambos(self, bot, update):
        gif = self.searchGif(["lamborghini"])
        bot.send_document(chat_id=update.message.chat_id, document=gif,caption="Boom!")
        # bot.send_message(chat_id=update.message.chat_id, text=gif)
    def gif (self, bot, update, args):
        gif = self.searchGif(args)
        if gif == "No gifs! Search again!":
            bot.send_message(chat_id=update.message.chat_id, text=gif)
        else:
            try:
                bot.send_document(chat_id=update.message.chat_id, document=gif,caption="Boom!")
            except:
                bot.send_message(chat_id=update.message.chat_id, text=gif)
        # bot.send_message(chat_id=update.message.chat_id, text="There are " + str(gif) + " gifs in this search")
    def searchGif (self, args):
        seed(datetime.now())
        for each in args:
            searchTerm =  "+".join(args)

        url1 = str("http://api.giphy.com/v1/gifs/")
        url2 = "search?q=" + searchTerm + "&api_key=ecJmwzf6vdD8fozImQtiqElIUIpmd4wR&limit=100"
        text = urljoin(url1, url2)

        data = json.load(urlopen(text))

        if len(data["data"]) == 0:
            return "No gifs! Search again!"
        elif len(data["data"]) == 1:
            i = 0
        else:
            i = randint(0,len(data["data"]))

        return (data["data"][i]["images"]["downsized"]["url"])
        # return length

    def help(self, bot, update):
        text = "Welcome to LamboBot2077!  \
        Available Commands:\
        \n/start: LamboBot2077 Intro\
        \n/lambos: sends a random lambo GIF\
        \n/gif [searchTerms 1 2 3]: sends a random GIF ex: /gif yo mama\
        \n/caps [yourTextHere]: echos your text"
        bot.send_message(chat_id=update.message.chat_id, text=text)

    def ticker (self, bot, update, args):
        if args[0].upper() == "U"   : symbol = args[1].upper() + "/USDT"
        elif args[0].upper() == "B" : symbol = args[1].upper() + "/BTC"
        elif args[0].upper() == "E" : symbol = args[1].upper() + "/ETH"
        else: symbol = "Error"

        if symbol == "Error" :
            bot.send_message(chat_id=update.message.chat_id, text=symbol)

        else:
            data = self.bit.fetch_ticker(symbol)
            msg = data["symbol"] + "\n" + \
                       "Ask:  "  + str(data["info"]["Ask"]) + "\n" + \
                       "Bid:  "  + str(data["info"]["Bid"]) + "\n" + \
                       "High: " + str(data["info"]["High"]) + "\n" + \
                       "Low:  "  + str(data["info"]["Low"])

            bot.send_message(chat_id=update.message.chat_id, text=msg)


def main():

    lb = lamboBot2077()




if __name__ == "__main__":
    main()
