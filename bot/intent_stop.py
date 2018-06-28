
#TODO finish
def check(user, msg):

    if "intent_stop_" in msg:
        if "intent_stop_0" == msg:
            msg = user.reset()
            
        elif "intent_stop_1" == msg:
            module.info_dict[recipient_id]["intent_stop"] = False
            last_return_value = module.info_dict[recipient_id]["last_return_value"]
            print("DEBUG:not STOP: info_dict:", module.info_dict[recipient_id])
            return last_return_value

    return user, msg