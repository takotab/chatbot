import logging
import datetime
from flask import current_app
from .user import User
from interact import interact

# possibly better with not holding everyone in memory
# also not so good if thing go wrong 
# currently need to update users in the end
users = {}


def message(recipient_id, msg):
    logging.info("bot.incoming_msg " + str(datetime.datetime.utcnow()) + " messeage from " +recipient_id + ":"+ msg)
    # return "hello " + str(recipient_id) + str(ink_story)
    try:
        user = users[recipient_id]
    except:
        logging.info("New recipient created id:" + recipient_id)
        user = User()  # initiating new story
    user.recieved_msg(msg)

    # reset inky
    if "$reset" in msg:
        msg = user.reset()

    msg = msg.replace("%20", " ")

    # calling controller method
    user, return_msg = interact(user = user, msg=msg)

    users[recipient_id] = user
    logging.info("bot.return_msg " + str(datetime.datetime.utcnow()) + " messeage to " +recipient_id + ":"+ return_msg)
    
    # cleaning up( not strickly nessary but clear)
    del user
    
    return return_msg

