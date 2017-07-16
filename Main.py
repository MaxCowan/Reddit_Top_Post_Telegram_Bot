#!/usr/bin/env python

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
from RedditInstance import RedditInstance

def start(bot, update):
    global flgInitialized
    if not flgInitialized:
        update.message.reply_text('Welcome to Reddit Conversation Starter 1.0\nType /help for more information.')
        flgInitialized = True
    else:
        update.message.reply_text('Bot is initialized.')


def help(bot, update):
    update.message.reply_text('Use the /grab command to initiate a conversation about any topic.\n'
                              'There are two ways to grab content:\n---------------------------\n"The first will prompt'
                              ' you with a custom keyboard that shows all the post timeline options, It looks like this:'
                              '\n/grab <subreddit name>\nEG: "/grab science"\n---------------------------\nThe second'
                              'usage requires a text argument following the subreddit you want to grab from. It looks'
                              ' like this:\n/grab <subreddit name> <timeline string>\nEG: "/grab funny all"\n'
                              'The 6 valid timeline strings are:\n---hour\n---day\n---week\n---month\n---year\n'
                              '---all\n---------------------------')

# Present the user with timeline options to refine their reddit query
def grab(bot, update, args):
    intCurrentChatID = update.message.chat_id
    # If user doesn't specify a timeline, present them with buttons
    if len(args) < 2:
        try:
            objKeyboard = [[InlineKeyboardButton("Past Hour", callback_data="0" + args[0]),
                        InlineKeyboardButton("Past Day", callback_data="1" + args[0]),
                        InlineKeyboardButton("Past Week", callback_data="2" + args[0])],
                        [InlineKeyboardButton("Past Month", callback_data="3" + args[0]),
                        InlineKeyboardButton("Past Year", callback_data="4" + args[0]),
                        InlineKeyboardButton("All Time", callback_data="5" + args[0])]]
            objReplyMarkup = InlineKeyboardMarkup(objKeyboard)
            update.message.reply_text('Select a timeline to retrieve top post from:', reply_markup=objReplyMarkup)

        except IndexError:
            update.message.reply_text("Please provide a subreddit to the grab command")
    # Specified a timeline with a second argument
    else:
        # Make sure timeline argument is valid
        if args[1] in arrTimelineStrings:
            # Repy to chat
            update.message.reply_text("Top Post ---> %s" % arrTimelines[arrTimelineStrings.index(args[1])])
            reply(bot, update, args[0], args[1], intCurrentChatID)
        else:
            update.message.reply_text("The second argument provided needs to be a valid timeline string."
                                      "\nFor examples of valid timeline strings type /help")


# When a keyboard button is pressed
def button(bot, update):
    # Store the callback data
    objQuery = update.callback_query
    # Extract the subreddit and timeline selection from the data
    intSelectedTimeline = int(objQuery.data[:1])
    strSubreddit = objQuery.data[1:]
    intCurrentChatID = objQuery.message.chat_id
    # Store edited post text
    strEdit = "Top Post ---> %s" % arrTimelines[intSelectedTimeline]
    # Transform the keyboard into the selected timeline
    bot.edit_message_text(text=strEdit,
                          chat_id=objQuery.message.chat_id,
                          message_id=objQuery.message.message_id)
    # Reply to chat
    reply(bot, update, strSubreddit, arrTimelineStrings[intSelectedTimeline], intCurrentChatID)


# Query Reddit
def getContent(strSub, strSelectedTimeline):
    return objReddit.grabPostContent(strSub, strSelectedTimeline)

# Format a reply after fetching content from Reddit
def reply(bot, update, strChosenSub, strSelectedTimeline, intChatID):
    arrContent = getContent(strChosenSub, strSelectedTimeline)
    # If there was not an error getting the content
    if len(arrContent) != 1:
        # Post is a self-post (text only)
        if arrContent[3]:
            strComments = "-----Self post-----" + '\n' + arrContent[1]
            bot.sendMessage(intChatID, strComments)
        # Post links to an external site
        else:
            strTitle = "-------Title-------" + '\n' + arrContent[0]
            strImage = arrContent[2]
            strComments = "-----Comments-----" + '\n' + arrContent[1]
            bot.sendMessage(intChatID, strTitle)
            # Attempt to send link as a photo
            try:
                bot.sendPhoto(intChatID, strImage)
            except:
                bot.sendMessage(intChatID, strImage)
            bot.sendMessage(intChatID, strComments)

    # Reply with the error message
    else:
        bot.sendMessage(intChatID, arrContent[0])


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("428735666:AAHrwoUKrplHx-cFrA5sqGCdgAF2iQbFoVw")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("grab", grab, pass_args=True))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    # Connect to objReddit
    objReddit = RedditInstance()

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Initialization flag
    flgInitialized = False

    # Options mapped to array indexes
    arrTimelines = ["Past Hour", "Past Day", "Past Week", "Past Month", "Past Year", "All Time"]
    # PRAW Reddit query inputs
    arrTimelineStrings = ['hour', 'day', 'week', 'month', 'year', 'all']

    main()
