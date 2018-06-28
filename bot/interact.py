from . import intent_stop 

def interact(user, msg):
    # function message
    user, msg = intent_stop.check(user = user,msg = msg)
    
    if len(ink_story[recipient_id].currentChoices):
        options = [ink_choice.text.replace("$button","").replace("$qr","") for ink_choice in ink_story[recipient_id].currentChoices]
        msg = nlpclient.match_text(msg, options)

    if "$choice_" in msg:
        msg_split = msg.split("_")
        print("controller is going to make choice ", msg_split[1])
        return inky_brain(ink_story, recipient_id, choice=msg_split[1])

    else:
        # normal message
        module.set_prev_intent(ink_story, recipient_id)
        ink_story = nlpclient.interpert_message(ink_story, recipient_id, msg)
        if module.info_dict[recipient_id]["prev_intent"] == "":
            check_intent(ink_story, recipient_id)
        return_value, stop = do_intent_stop_stuff(ink_story, recipient_id)
        if stop:
            print("stop == ", stop)
            return return_value
        # if module.ink_handel.get_variable(ink_story, recipient_id, "nlp_newinfo"):
        #     # print("changed something!!")
        #     return inky_brain(ink_story= ink_story, recipient_id= recipient_id, choice = 0)
        return inky_brain(ink_story=ink_story,
                          recipient_id=recipient_id,
                          choice=None)
