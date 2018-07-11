import logging
import time
import datetime
import codecs
import clr # pylint: disable=E0401
from flask import Flask, current_app
from .weather import weather
import os
from .nlp import nlp_class
from . import modules as Modules
from .attachement import check_attachement_str

# Global Variables
end_of_text = "XDISCONNECT"
path_engine = os.path.join(os.getcwd(), "ink", "ink-engine-runtime.dll")
ink_file = os.path.join(os.getcwd(), "ink", "current_inky.ink")
# ink_file = os.path.join(os.getcwd(), "ink", "alt_test_inky_tako.ink")
path_ink_json = ink_file + ".json"

command = 'mono ' + os.path.join(os.getcwd(),
                                 "ink", "inklecate.exe") + " " + ink_file
logging.info(command)
os.system(command)

clr.AddReference(path_engine)
with codecs.open(path_ink_json, 'r', 'utf-8-sig') as data_file:
    ink_json = data_file.read()
from Ink.Runtime import Story  # pylint: disable=E0401

ink_story = {}
return_value = {}
app = Flask(__name__)
module = Modules.modules()

nlpclient = nlp_class(module)
import entity_rec


def reset(recipient_id):
    del ink_story[recipient_id]
    module.start_id(recipient_id)
    init_recipient(recipient_id)
    msg = " "
    return msg

# story for every recipient


def init_recipient(recipient_id):
    ink_story[recipient_id] = Story(ink_json)


def interact(ink_story, recipient_id, msg):
    print("controller", recipient_id, msg)
    # function message
    if "intent_stop_" in msg:
        if "intent_stop_0" == msg:
            msg = reset(recipient_id)
        elif "intent_stop_1" == msg:
            module.info_dict[recipient_id]["intent_stop"] = False
            last_return_value = module.info_dict[recipient_id]["last_return_value"]
            print("DEBUG:not STOP: info_dict:", module.info_dict[recipient_id])
            return last_return_value

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


def inky_brain(ink_story, recipient_id, choice=None):
    next_ = ""

    if choice is not None:
        print("choice", choice)
        try:
            ink_story[recipient_id].ChooseChoiceIndex(int(choice))  # 0
        except:
            print("error in making choice")
        print("made choice:", choice)

        # ink_story = check_intent(ink_story, recipient_id)
    i = 0
    return_value = {}
    return_value[recipient_id] = ""
    while ink_story[recipient_id].canContinue and \
            not module.get_wait(recipient_id):

        next_ = ink_story[recipient_id].Continue().replace("—", "-")
        print("next_", next_)
        if next_.startswith("$"):
            list_w_ink_outputs = next_[1:].replace("\n", "").split(',')
            print(list_w_ink_outputs)
            if list_w_ink_outputs[0].lower() == 'weather':

                ink_story = module.weatherfunc(ink_story, recipient_id,
                                               loc=list_w_ink_outputs[1],
                                               time=list_w_ink_outputs[2])
            if next_.startswith("$sql"):
                ink_story = module.f_sql(
                    ink_story, recipient_id, list_w_ink_outputs)
                print("wait 0.5", i)
                time.sleep(0.5)
                i += 1
                print("wait 0.5")
            if next_.startswith("$vacation"):
                ink_story = module.vacation(
                    ink_story, recipient_id, list_w_ink_outputs)
            if next_.startswith("$write"):
                ink_story = module.write(
                    ink_story, recipient_id, list_w_ink_outputs)
            if next_.startswith("$postcode_nl"):
                ink_story = module.postcode_nl(
                    ink_story, recipient_id, list_w_ink_outputs)
            if next_.startswith("$plan_meeting"):
                ink_story = module.plan_meeting(ink_story, recipient_id)
            if next_.startswith("$make_meeting"):
                ink_story = module.make_meeting(ink_story, recipient_id)
            if next_.startswith("$wait"):
                ink_story = module.wait(ink_story, recipient_id, next_)
            
            ink_story, return_value = check_attachement_str(next_, module, recipient_id, ink_story, return_value)

            if next_.startswith("$sql_vergelijken"):
                ink_story = module.sql_vergelijken(ink_story, recipient_id)
            if next_.startswith("$intent_direct"):
                check_intent(ink_story, recipient_id)
            next_ = ""
        elif next_.startswith("%"):
            next_ = ""
        
        return_value[recipient_id] += str(next_) + '\n'

        print("cancontinue = ", ink_story[recipient_id].canContinue,
              "wait =", module.get_wait(recipient_id),
              "stop = ", )
    # print("i can not continue", "wait = ", module.get_wait(recipient_id))

    if len(ink_story[recipient_id].currentChoices) > 0 and \
            not module.get_wait(recipient_id):
        print("Debug: Narrative session handler: Making menu options",
              len(ink_story[recipient_id].currentChoices))
        for i in range(len(ink_story[recipient_id].currentChoices)):
            text_options = ink_story[recipient_id].currentChoices[i].text.replace(
                "—", "-")
            if not text_options.startswith("%"):
                if "$button" in text_options:
                    print("Debug: Narrative session handler: Button recognized")
                    return_value[recipient_id] += str(text_options) 
                else:
                    return_value[recipient_id] += "$qr" + str(text_options)

    if next_.__contains__(end_of_text) or "$reset" in next_:
        print("end of story")
        del ink_story[recipient_id]
    if not return_value[recipient_id] == "":
        module.info_dict[recipient_id]["last_return_value"] = return_value[recipient_id]
    print("DEBUG:not STOP: info_dict:", module.info_dict[recipient_id])

    return ink_story, return_value[recipient_id]


def check_intent(ink_story, recipient_id):

    intent = module.get_variable(ink_story, recipient_id, "intent")
    print("Debug: check_intent: going to check if we can move. \nIntent:", intent)
    if "dwg_" in intent:
        new_loc = "intent_dwg.vraag" + str(intent.split("_")[1])
        print("Debug: Narrative session handler: Go to", new_loc)
        ink_story = module.goto_knot(ink_story, recipient_id, new_loc)
    elif "waterstand_doorgeven" == intent:
        new_loc = "waterstand.doorgeven"
        print("Debug: Narrative session handler: Go to", new_loc)
        ink_story = module.goto_knot(ink_story, recipient_id, new_loc)
    elif "waterstand_vergelijken" == intent:
        new_loc = "waterstand.vergelijken"
        print("Debug: Narrative session handler: Go to", new_loc)
        ink_story = module.goto_knot(ink_story, recipient_id, new_loc)
    elif "factuur" == intent:
        new_loc = "factuur"
        print("Debug: Narrative session handler: Go to", new_loc)
        ink_story = module.goto_knot(ink_story, recipient_id, new_loc)
    elif "weather" == intent:
        new_loc = "function_weather.call"
        print("Debug: Narrative session handler: Go to", new_loc)
        ink_story = module.goto_knot(ink_story, recipient_id, new_loc)
    elif "vacation" == intent:
        new_loc = "vacation"
        print("Debug: Narrative session handler: Go to", new_loc)
        ink_story = module.goto_knot(ink_story, recipient_id, new_loc)
    elif 'address_change' == intent:
        new_loc = "address_change"
        print("Debug: Narrative session handler: Go to", new_loc)
        ink_story = module.goto_knot(ink_story, recipient_id, new_loc)

    return ink_story


def do_intent_stop_stuff(ink_story, recipient_id):
    _return_value = ""
    stop = module.get_variable(ink_story, recipient_id, "intent") == "stop"
    if recipient_id not in module.info_dict:
        module.start_id(recipient_id)
    module.info_dict[recipient_id]["intent_stop"] = stop
    if stop:
        _return_value = "Weet je zeker dat je wilt stoppen met wat je aan het doen was?\n"
        _return_value += "$button Jazeker %%intent_stop_0\n"
        _return_value += "$button Neen %%intent_stop_1\n"

    return _return_value, stop
