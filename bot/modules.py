import json
import sys
import calender_app.calender_app as cal_app
from flask import Flask
from .weather import weather
from .nlp import nlp_class
from . import sqlite
from . import vacationdays
from . import postcode as Postcode
from . import make_image as make_image


class modules:
    def __init__(self):

        self.cal = None
        self.group_dict = {
            "DWG Devo": ["Rob van der Heiden",
                         "Roger van Daalen",
                         "Paul Settels",
                         "Walter Snel"],
            "Sales": ["Melis Schaap",
                      "Antoin van der Ben",
                      "Hans Beugelink",
                      "Rob van der Heiden",
                      "Sjoerd Veen",
                      "Marco Croese"],
            "BM": ["Marc Bovy",
                   "Ratko Popovski",
                   "Hans Mollevanger",
                   "Chris Hau",
                   "Marc Kikkert"
                   ],
            "BM + Sales": ["Melis Schaap",
                           "Antoin van der Ben",
                           "Hans Beugelink",
                           "Rob van der Heiden",
                           "Sjoerd Veen",
                           "Marco Croese",
                           "Marc Bovy",
                           "Ratko Popovski",
                           "Hans Mollevanger",
                           "Chris Hau",
                           "Marc Kikkert"],
            "Team AI": ["tako tabak", "roger van daalen",
                        "dimitrios lerios",
                        "sibren jansen"],
            "Team DL": ["tako tabak", 'walter snel']
        }
        self.info_dict = {}

    def start_id(self, recipient_id):
        print("new id made in modules")
        self.info_dict = {recipient_id: {"wait": False,
                                         "_wait_var_to_be_changed": [],
                                         "_num_wait_var": None,
                                         "current_knot": None,
                                         "intent_stop": False,
                                         "intent_asked": False,
                                         "last_return_value": "",
                                         "prev_intent": ""}}

    def set_prev_intent(self, ink_story, recipient_id):
        self.start_id(recipient_id)
        c_intent = self.get_variable(
            ink_story, recipient_id, "intent")

        if c_intent is not "stop":
            self.info_dict[recipient_id]["prev_intent"] = c_intent

    def get_wait(self, recipient_id):
        if recipient_id not in self.info_dict:
            self.start_id(recipient_id)
            self.info_dict[recipient_id]["wait"] = False

        return self.info_dict[recipient_id]["wait"]

    def set_wait(self, recipient_id, value):
        if recipient_id not in self.info_dict:
            self.start_id(recipient_id)
        self.info_dict[recipient_id]["wait"] = value
        return self.info_dict[recipient_id]["wait"]

    def wait(self, ink_story, recipient_id, text):
        self.set_wait(recipient_id, True)
        self.make_wait_check(recipient_id, text)
        return ink_story

    def make_wait_check(self, recipient_id, text):
        split_text = text.replace("\n", '').split(",")
        print(split_text)
        if len(split_text) == 1:  # no extra info wait on something to be changed
            self.info_dict[recipient_id]["_num_wait_var"] = 1
            self.info_dict[recipient_id]["_wait_var_to_be_changed"] = []
        else:
            self.info_dict[recipient_id]["_num_wait_var"] = int(split_text[1])
            self.info_dict[recipient_id]["_wait_var_to_be_changed"] = [
                var for var in split_text[2:]]

    def wait_check(self, recipient_id, key):
        if recipient_id not in self.info_dict:
            self.start_id(recipient_id)

        # print("wait check", self.info_dict[recipient_id])
        if self.info_dict[recipient_id]["_num_wait_var"] is None:
            pass
        elif self.info_dict[recipient_id]["_num_wait_var"] == 1 and self.info_dict[recipient_id]["_wait_var_to_be_changed"] == []:
            #  just one variable to be changed
            self.set_wait(recipient_id, False)
            self.info_dict[recipient_id]["_wait_var_to_be_changed"] = []
            self.info_dict[recipient_id]["_num_wait_var"] = None
        else:
            t_wait_var_to_be_changed = self.info_dict[recipient_id]["_wait_var_to_be_changed"].copy(
            )
            for var in t_wait_var_to_be_changed:
                bool_ = str(key).replace(" ", "") == str(var).replace(" ", "")
                if bool_:
                    print("debug key:",key," and var: ",var," and same ", bool_)
                    self.info_dict[recipient_id]["_wait_var_to_be_changed"].remove(
                        var)
                    self.info_dict[recipient_id]["_num_wait_var"] -= 1

            print("_num_wait_var :",
                  self.info_dict[recipient_id]["_num_wait_var"])
            if 0 >= self.info_dict[recipient_id]["_num_wait_var"]:
                self.set_wait(recipient_id, False)
                self.info_dict[recipient_id][""] = []
                self.info_dict[recipient_id]["_num_wait_var"] = None

    def set_variable(self, ink_story, recipient_id, key, value):
        #        if not ink_story[recipient_id].variablesState[key] == "":
     #           ink_story[recipient_id].variablesState[key + "_previous_query"] = ink_story[recipient_id].variablesState[key]
        try_went_well = False
        try:
            ink_story[recipient_id].variablesState[key] = value
            ink_story[recipient_id].variablesState["nlp_newinfo"] = 1
            try_went_well = True
        except:
            print("could not write to inky", key, value)
            print("debug error message", sys.exc_info())

        if try_went_well:
            self.wait_check(recipient_id, key)

        try:
            ink_story[recipient_id].variablesState[key + "_defined"] = 1
        except:
            # print("failed to set", key + "_defined")
            pass

    def get_variable(self, ink_story, recipient_id, key):
        return_value = ink_story[recipient_id].variablesState[key]
        if return_value is None:
            return_value = "NOT FOUND"
        return return_value

    def goto_knot(self, ink_story, recipient_id, knot_stitch):
        ink_story[recipient_id].ChoosePathString(knot_stitch, None, None)

        return ink_story

    def update_state(self, ink_story, recipient_id):
        _state = ink_story[recipient_id].state
        t = self.get_knot_out(_state.ToJson())
        print("debug ink state", t)
        try:
            self.info_dict[recipient_id]["current_knot"] = t
        except:
            pass

    def get_knot_out(self, json_str):
        json_ = json.loads(json_str)
        print(json_)

        knot = json_["callstackThreads"]  # callstackthre
        knot = knot["threads"]  # threads
        knot = knot[0]  # 0
        knot = knot["callstack"]
        knot = knot[0]  # 0
        knot = knot["temp"]
        knot = knot["$r"]["^->"].split(".")
        print(knot)
        for i, part in enumerate(knot):
            if part.isdigit():
                print(part, knot, i)
                return ".".join(knot[:i])

    def weatherfunc(self, ink_story, recipient_id, loc='', time=''):
        print("weatherfunc(", loc, time)
        # try:
        if "nu" in time:
            time = "now"
        elif "morgen" in time:
            time = "tomorrow"
        elif 'vandaag' in time:
            time == "now"
        loc = loc.strip()
        time = time.strip()
        # try:
        print(loc, " ", time)
        status, temp = weather(loc, time, language_='nl')
        # except:
        #   return 'please, enter a valid inputs'
        print("recived weather:", status, temp)
        # setting Inky variables
        self.set_variable(ink_story, recipient_id, "f_temperature", temp)
        self.set_variable(ink_story, recipient_id, "f_weather", status)
        return ink_story
        # except:
        #   print("problem while getting weather")
        #   return ink_story

    def f_sql(self, ink_story, recipient_id, list_w_ink_outputs):
        if list_w_ink_outputs[0].lower() == 'sql_w':
            print(list_w_ink_outputs)
            user_id = self.get_variable(ink_story, recipient_id, 'sql_id')
            target_value = self.get_variable(
                ink_story, recipient_id, list_w_ink_outputs[1])
            target_str = list_w_ink_outputs[1] + "=\'" + target_value + "\'"
            print("change", " data = ", user_id, " target =", target_str)
            sqlite.do_stuff("change", data=user_id, target=target_str)
            print("sql_w complete")

        elif list_w_ink_outputs[0].lower() == "sql_r":
            outvalue = self.sql_r(ink_story, recipient_id,
                                  list_w_ink_outputs[1])
            # print("outvalue", outvalue)

            self.set_variable(ink_story, recipient_id,
                              list_w_ink_outputs[1], outvalue)

            if not outvalue == "0":
                self.set_variable(ink_story, recipient_id,
                                  'user_identified', 1)
                print("user_identified =", 1, outvalue == "0")
        return ink_story

    def sql_vergelijken(self, ink_story, recipient_id):
        # get int_vergelijken

        dwg_water_expected = self.sql_r(
            ink_story, recipient_id, "dwg_water_expected")
        dwg_water_real = self.sql_r(ink_story, recipient_id, "dwg_water_real")
        print("Debug:sql_vergelijken: dwg_water_expected = ",
              dwg_water_expected, "dwg_water_real = ", dwg_water_real)
        int_vergelijken = round(
            float(dwg_water_real) / float(dwg_water_expected), 1)
        self.set_variable(ink_story, recipient_id,
                          "int_vergelijken", int_vergelijken)
        return ink_story

    def sql_r(self, ink_story, recipient_id, value):
        # print("starting sql_r", value)
        dict_data = {}
        for name in ["sql_id", "nlp_f_name", "nlp_l_name"]:  # nlp_dob
            dict_data[name] = self.get_variable(
                ink_story, recipient_id, name)
            if dict_data[name] == None or dict_data[name] == 0 or dict_data[name] == "" or dict_data[name] == "0":
                del dict_data[name]

        str_dict_data = str(dict_data)
        # print("str_dict_data", str_dict_data)
        outvalue = sqlite.do_stuff(
            "print", str_dict_data, value)
        # print("debug sql_r outvalue =", outvalue)
        return outvalue

    def vacation(self, ink_story, recipient_id, list_w_ink_outputs):
        print("starting vacation")
        true_name_ = (self.get_variable(ink_story, recipient_id, 'nlp_f_name') + " " +
                      self.get_variable(ink_story, recipient_id, 'nlp_l_name'))
        sql_id = self.get_variable(ink_story, recipient_id, 'sql_id')
        dict_, filename = vacationdays.get_plot_from_sql(
            'sqlite/random_table_dwg.db', sql_id, true_name=true_name_)
        print(dict_, filename)
        self.set_variable(ink_story, recipient_id, "vacation_days", str(dict_))

        self.set_variable(ink_story, recipient_id,
                          "filename_vacation", filename)

        return ink_story

    def postcode_nl(self, ink_story, recipient_id, list_w_ink_outputs):
        if len(list_w_ink_outputs) == 3:
            housenumber, postcode = list_w_ink_outputs[1:]
            street, municipality, province = Postcode.getpostcode(
                housenumber, postcode)
            # sql_id,nlp_f_name,nlp_l_name,sql_dob,sql_street,sql_postcode,sql_city
            self.set_variable(ink_story, recipient_id, "sql_street", street)
            self.set_variable(ink_story, recipient_id,
                              "sql_city", municipality)
            return ink_story
        else:
            return "error"

    def write(self, ink_story, recipient_id, list_w_ink_outputs):
        if len(list_w_ink_outputs) == 3:
            orgin_key, new_key = list_w_ink_outputs[1:]
            orgin_var = self.get_variable(ink_story, recipient_id, orgin_key)
            self.set_variable(ink_story, recipient_id, new_key, orgin_var)
            print(new_key, "has become ", orgin_var)
            return ink_story
        return "error"

    def handel_face(self, ink_story, recipient_id, msg):
        # face:
        # Walter Snel: 0.27503738001242567
        msg_split = msg.split("\n")
        name, certenty = msg_split[1].split(":")
        if float(certenty) > 0.2:
            f_name_l_name = name.split(" ")
            f_name = None
            for name in f_name_l_name:
                if len(name) > 0 and f_name is None:
                    f_name = name
                elif f_name is not None:
                    l_name = name
                else:
                    pass

            self.set_variable(ink_story, recipient_id, "nlp_f_name", f_name)
            self.set_variable(ink_story, recipient_id, "nlp_l_name", l_name)

    def plan_meeting(self, ink_story, recipient_id):
        """
        write
            {_location}
            {_date}
            {_time}
            {_duration}
        """
        self.cal = cal_app.calender_app()
        group_name = self.get_variable(ink_story, recipient_id, 'meeting_ids')
        names = self.group_dict[group_name]
        start_search = self.get_variable(
            ink_story, recipient_id, 'start_meeting')
        start, end_ = self.cal.main(names=names, start_search=start_search)
        day_str, time_str = self.cal.meeting_to_string()
        print("debug meeting time and date to string:", day_str, time_str)
        self.set_variable(ink_story, recipient_id,
                          '_location', self.cal.loc['name'])
        self.set_variable(ink_story, recipient_id, '_date', day_str)
        self.set_variable(ink_story, recipient_id, '_time', time_str)
        # self.set_variable(ink_story, recipient_id, '_duration', 30)

        return ink_story

    def make_meeting(self, ink_story, recipient_id):
        """
        write _link and _unique_id
        """
        link, event = self.cal.make_event()
        print("link to event:", link)
        self.set_variable(ink_story, recipient_id, '_link_meeting', link)
        self.event = event
        return ink_story

    def verhuizen_attachment(self, ink_story, recipient_id):
        # new {nlp_street} {nlp_postcode} {nlp_loc}
        # old {sql_street} {sql_postcode} {sql_city}
        info = ["nlp_street", "nlp_postcode", "nlp_loc",
                "sql_street", "sql_postcode", "sql_city"]
        info_dict = {}
        for name in info:
            value = self.get_variable(ink_story, recipient_id, name)
            info_dict[name] = value
        filename = make_image.make_image_verhuizen(
            info_dict, str(recipient_id))
        return ink_story, filename

    def factuur_attachment(self, ink_story, recipient_id):
        # new {nlp_street} {nlp_postcode} {nlp_loc}
        # old {sql_street} {sql_postcode} {sql_city}
        persoonsgegevens = ["sql_city", "sql_street", "sql_postcode",
                            "sql_id", "nlp_f_name", "nlp_l_name"]

        info_dict = {}
        for name in persoonsgegevens:
            outvalue = self.sql_r(ink_story, recipient_id, name)
            # print("outvalue", outvalue)
            self.set_variable(ink_story, recipient_id,
                              name, outvalue)
            value = self.get_variable(ink_story, recipient_id, name)
            if not outvalue == value:
                print(
                    "something went horribly wrong not outvalue == value", outvalue, value)
            info_dict[name] = value
        info_dict["invoice_period"] = "22-09-2017 tot 10-01-2018"

        filename = make_image.make_image_factuur(str(recipient_id), info_dict)
        return ink_story, filename

    def vergelijken_attachment(self, ink_story, recipient_id):
        # get int_vergelijken
        info_dict = {}
        info_dict["waterstand_norm"] = self.sql_r(
            ink_story, recipient_id, "dwg_water_expected")
        info_dict["waterstand"] = self.sql_r(
            ink_story, recipient_id, "dwg_water_real")
        print("Debug:vergelijken_attachment: dwg_water_expected = ",
              info_dict["waterstand_norm"], "dwg_water_real = ", info_dict["waterstand"])
        info_dict["vergelijking"] = str(round(
            100 * (float(info_dict["waterstand"]) / float(info_dict["waterstand_norm"])), 1))
        filename = make_image.make_image_vergelijken(
            str(recipient_id), info_dict)
        return ink_story, filename

    def check_intent_stop(self, ink_story, recipient_id):

        intent = self.get_variable(ink_story, recipient_id, "intent")
        if intent == "stop":
            self.info_dict[recipient_id]["intent_stop"] = True

        return ink_story

    def get_stop_intent(self, recipient_id):
        return self.info_dict[recipient_id]["intent_stop"]
