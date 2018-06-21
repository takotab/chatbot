class ink_handeler_class:
    def __init__(self):
        self.list_w_variables = ["nlp_loc",
                                "nlp_time",
                                 "nlp_f_name",
                                  "nlp_l_name",
                                  "nlp_postcode",
                                  "nlp_straatnaam",
                                  "weather_goal" ]

    def reset(self, ink_story, recipient_id):
        for key in self.list_w_variables:

            ink_story[recipient_id].variablesState[key] = ""
            try:
                ink_story[recipient_id].variablesState[key + "_defined"] = "False"
            except:
                print("failed to set", key + "_defined")
        ink_story[recipient_id].variablesState["started"] = 1

    def set_variable(self, ink_story, recipient_id, key, value):
#        if not ink_story[recipient_id].variablesState[key] == "":
 #           ink_story[recipient_id].variablesState[key + "_previous_query"] = ink_story[recipient_id].variablesState[key]
        try:
            ink_story[recipient_id].variablesState[key] = value
            ink_story[recipient_id].variablesState["nlp_newinfo"] = 1
        except:
            print("could not write to inky", key,value)
        try:
            ink_story[recipient_id].variablesState[key + "_defined"] = 1
        except:
            # print("failed to set", key + "_defined")
            pass

    def get_variable(self, ink_story, recipient_id, key):
        return ink_story[recipient_id].variablesState[key]
