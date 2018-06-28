from ink_story import Story, ink_json



class User():

    def __init__(self):
        self.start()

    def start(self):
        self.ink_story= Story(ink_json)
        self.info_dict = {"wait": False,
                        "_wait_var_to_be_changed": [],
                        "_num_wait_var": None,
                        "current_knot": None,
                        "intent_stop": False,
                        "intent_asked": False,
                        "last_return_value": "",
                        "prev_intent": "",}
        try:
            self.conversation.append(" <RESET> ")
        except:
            self.conversation = []


    def reset(self):
        self.start()
        msg = " "
        return msg

    def recieved_msg(self,msg):
        self.conversation.append("USER:" + msg)

    def send_msg(self,return_msg):
        self.conversation.append("TINA:" + return_msg)



