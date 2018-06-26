# import entity_rec
import urllib.request
import json
import re
# from flask import current_app
CONFIDENCE_LEVEL = 0.8


class nlp_class:
    def __init__(self, module):
        self.module = module

    def match_text(self, value, options):
        """
        Will check if value has a high probality (cos sim) to one of the options.

        input:
            Value   str of userinput
            options the options that the text could be

        The return depends on the confince level so
            - if the confidence if high enough than "choice_" + option index
            - otherwise just the msg


        """
        return "$choice_0" 
        choice = entity_rec.match_text(value, options)
        if choice["confidence"] > CONFIDENCE_LEVEL:
            return "$choice_" + str(choice["choice"])
        return value

    def interpert_message(self, ink_story, recipient_id, msg):
        if ink_story[recipient_id].variablesState["started"] == False:
            self.module.reset(ink_story, recipient_id)
        print("Debug: NLP: Processing ", msg)
        # web_msg = msg.replace(" ", "%20")
        # dt/text/entities?text=
        resp = None

        if not len(msg.replace(" ", "")):
            return ink_story
        return ink_story
        resp = entity_rec.predict(msg)
        try:
            pass
            # url = 'http://0.0.0.0:5081/dt/text/entities?text=' + web_msg
            # print("url", url)
            # response = urllib.request.urlopen(url)
            # resp = response.read().decode('UTF-8')
            # print("response",resp.replace("\n","--"))
        except:

            print("Debug: NLP: No entities found")
        print(resp)
        if not resp == None:
            # resp = json.loads(resp)
            for key in resp:
                obj = resp[key]
                if float(resp[key]["confidence"]) < CONFIDENCE_LEVEL or key is 'intent_unknown':
                    print("not sure about", obj, "break")
                else:

                    value = obj["text"]
                    #  {'entityName': 'intent_unknown', 'entityScore': '0', 'entityValue':True}
                    if key.startswith("intent_"):
                        key = key.replace("intent_", "")
                        print("Debug: NLP: intent_ ", key, " detected")
                        if key == "unkown":
                            print("Debug: NLP: key = ", key, "break")
                        elif key == "stop" and len(msg.split(" ")) > 1:
                            print("Debug: NLP: key = ", key, "too long",
                                  len(msg.split(" ")), "break")

                        self.module.set_variable(
                            ink_story, recipient_id, "intent", key)

                    else:
                        print(value, " detected as ", key)
                        if key in ["nlp_f_name", "nlp_l_name"] and value[0].islower():
                            print("Debug:NLP: to upper")
                            value = value[0].upper() + value[1:]

                        self.module.set_variable(
                            ink_story, recipient_id, key, value)

        else:
            print("Debug: NLP: Some type of error")

        goal_legend = ["unknown", "context_weather",
                       "context_sql_lookup", "context_sql_change", "context_sql_count"]
        if "morgen" in msg:
            self.module.set_variable(
                ink_story, recipient_id, "nlp_time", "morgen")
            print(
                "Debug: Rule-based NLP: variable *nlp_time* set as *morgen* based on *morgen* keyword")
        if 'nu' in msg or 'vandaag' in msg:
            self.module.set_variable(ink_story, recipient_id, "nlp_time", "nu")
            print(
                "Debug: Rule-based NLP: variable *nlp_time* set as *nu* based on *nu/vandaag* keyword")
        if "weer" in msg:
            print("Debug: Rule-based NLP:", "intent set as",
                  "*weather*", "based on", "*weer*", "keyword")
            self.module.set_variable(
                ink_story, recipient_id, "intent", "weather")
        for goal_ in goal_legend:
            if goal_ in msg:
                print(goal_, "detected", "hard")
                self.module.set_variable(ink_story, recipient_id, goal_, "1")
        if 'verhuizen' in msg:
            print(
                "Debug: Rule-based NLP: intent set as *verhuizen* based on *verhuizen* keyword")
            self.module.set_variable(
                ink_story, recipient_id, "context_sql_lookup", "1")
            self.module.set_variable(
                ink_story, recipient_id, "context_weather2", "0")
        if 'vakantie' in msg:
            print("vakantie", "detected", "hard")
            self.module.set_variable(
                ink_story, recipient_id, "intent", "vacation")
            self.module.set_variable(
                ink_story, recipient_id, "context_sql_count", "1")
            self.module.set_variable(
                ink_story, recipient_id, "context_sql_lookup", "0")
            self.module.set_variable(
                ink_story, recipient_id, "context_weather", "0")

        digits = re.findall("(\d+)", msg)
        if len(digits):
            for dig in digits:
                print("Debug: Rule-based NLP: entity set as " +
                      str(dig) + " based on *digigts*")
                self.module.set_variable(
                    ink_story, recipient_id, "number", str(dig))

        postcode = re.findall("[0-9][0-9][0-9][0-9][A-Z][A-Z]", msg)
        if len(postcode):
            for code in postcode:
                print("Debug: Rule-based NLP: entity set as " +
                      str(code) + " based on *postcode*")
                self.module.set_variable(
                    ink_story, recipient_id, "nlp_postcode", str(code))

        straat = re.findall(
            "([A-z]*)(laan|hof|straat|pad|markt|kade|boulevard|tuin|hof|steeg])( )([0-z]*)", msg)
        if len(straat):
            for stra in straat:
                stra = "".join(stra)
                print("Debug: Rule-based NLP: entity set as " +
                      str(stra) + " based on *street*")
                self.module.set_variable(
                    ink_story, recipient_id, "nlp_street", str(stra))
        ink_story = self.hard_detect(ink_story, recipient_id, msg)
        return ink_story

    def hard_detect(self, ink_story, recipient_id, msg):
        dict_with_regex = {"(\d+)": {"key": "number"},
                           "[0-9][0-9][0-9][0-9][A-Z][A-Z]": {"key": "nlp_postcode"},
                           "([A-z]*)(laan|hof|straat|pad|markt|kade|boulevard|tuin|hof|steeg])( )([0-z]*)":
                           {"key": "nlp_street"},
                           "(thuis.*vesta.*pro)": {"key": "intent_dwg_7", "case_insenstive": False},
                           "(vesta.*pro.*thuis)": {"key": "intent_dwg_7", "case_insenstive": False},
                           "(datafreeze)": {"key": "intent_dwg_13", "case_insenstive": False},
                           "(recuperatieverlof.*glijsaldo.*negatief)": {"key": "intent_dwg_20", "case_insenstive": False},
                           "(recuperatieverlof.*negatief.*glijsaldo)": {"key": "intent_dwg_20", "case_insenstive": False},
                           "(negatief.*glijsaldo.*recuperatieverlof)": {"key": "intent_dwg_20", "case_insenstive": False},
                           "(glijsaldo.*negatief.*recuperatieverlof)": {"key": "intent_dwg_20", "case_insenstive": False},
                           "(tikkingen)": {"key": "intent_dwg_21", "case_insenstive": False},
                           "(inhaalrust)": {"key": "intent_dwg_25", "case_insenstive": False},
                           "verlofaanvraag.*(Outlook)": {"key": "intent_dwg_26", "case_insenstive": False},
                           "verlofaanvraag.*([e\s]mail)": {"key": "intent_dwg_26", "case_insenstive": False},
                           "(Outlook).*verlofaanvraag": {"key": "intent_dwg_26", "case_insenstive": False},
                           "([e\s]mail).*verlofaanvraag": {"key": "intent_dwg_26", "case_insenstive": False},
                           "(verlof).*(uren)": {"key": "intent_dwg_27", "case_insenstive": False},
                           "(verlof).*(dag)": {"key": "intent_dwg_27", "case_insenstive": False},
                           "(uren).*(verlof)": {"key": "intent_dwg_27", "case_insenstive": False},
                           "(dag).*(verlof)": {"key": "intent_dwg_27", "case_insenstive": False},
                           "Tako": {"key": "nlp_f_name", "case_insenstive": True},
                           "Tabak": {"key": "nlp_l_name", "case_insenstive": True},
                           }
        for regex in dict_with_regex:
            if "case_insenstive" in dict_with_regex[regex]:
                if not dict_with_regex[regex]["case_insenstive"]:
                    entity = re.findall(regex, msg, re.IGNORECASE)
                else:
                    entity = re.findall(regex, msg)
            else:
                entity = re.findall(regex, msg)

            if len(entity):
                key = dict_with_regex[regex]["key"]
                for value in entity:
                    value = "".join(value)
                    if key.startswith("intent_"):
                        key = key.replace("intent_", "")
                        print("Debug: Rule-based NLP: intent " +
                              key + " set as " + str(True))
                        self.module.set_variable(ink_story, recipient_id,
                                                 'intent', key)
                    else:
                        print("Debug: Rule-based NLP: entity " +
                              key + " set as " + str(value))

                        self.module.set_variable(ink_story, recipient_id,
                                                 key, str(value))

        return ink_story


def change_key(key):
    dict_of_keys = {'nlp_l_name': "nlp_f_name", 'nlp_loc': 'nlp_l_name',
                    "nlp_time": 'nlp_loc', 'nlp_city': 'nlp_postcode',
                    'nlp_postcode': 'nlp_street', 'nlp_dob': 'nlp_dob'}
    if key in dict_of_keys:
        print("from ", key, "to", dict_of_keys[key])
        key = dict_of_keys[key]
    return key
