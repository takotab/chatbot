import logging
import datetime
from flask import current_app

from user import User
from .session_handler import interact

# possibly better with not holding everyone in memory
# also not so good if thing go wrong 
# currently need to update users in the end
users = {}

def message(recipient_id, msg):
    logging.info("bot.incoming_msg " + str(datetime.datetime.utcnow()) + " messeage from " +recipient_id + ":"+ msg)

    try:
        user = users[recipient_id]
    except:
        logging.info("New recipient created id:" + recipient_id)
        user = User(recipient_id)  # initiating new story

    
    msg = msg.replace("%20", " ")
    user.recieved_msg(msg)

    # reset inky
    if "$reset" in msg:
        msg = user.reset()

    user, return_msg = interact(ink_story=user,
                     recipient_id=recipient_id, msg=msg)

    users[recipient_id] = user


    logging.info("bot.return_msg " + str(datetime.datetime.utcnow()) + " messeage to " +recipient_id + ":"+ return_msg)

    # cleaning up( not strickly nessary but clear)
    del user

    return return_msg