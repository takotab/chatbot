import entity_rec
CONFIDENCE_LEVEL = 0.8

def match_text(value, options):
        """
        Will check if value has a high probality (cos sim) to one of the options.

        input:
            Value   str of userinput
            options the options that the text could be
        
        The return depends on the confince level so
            - if the confidence if high enough than "choice_" + option index
            - otherwise just the msg
        

        """
        choice = entity_rec.match_text(value,options)
        if choice["confidence"] > CONFIDENCE_LEVEL:
            return "$choice_" +  str(choice["choice"])
        return value