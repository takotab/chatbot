from flask import current_app
ATTACHMENT_END = current_app.config["ATTACHMENT_END"]
ATTACHMENT_START = current_app.config["ATTACHMENT_START"]


def check_attachement_str(next_, module,recipient_id,ink_story,return_value):
    if next_.startswith("$attachment"):
        print("atttachemt")
        return_value[recipient_id] += ATTACHMENT_START + str(next_) \
        + ATTACHMENT_END + '\n'        
        print("added to return_value", next_)

    if next_.startswith("$verhuizen_attachment"):
        ink_story, filename = module.verhuizen_attachment(
            ink_story, recipient_id)
        return_value[recipient_id] += ATTACHMENT_START + \
            str(filename) + ATTACHMENT_END + '\n'
    if next_.startswith("$factuur_attachment"):
        ink_story, filename = module.factuur_attachment(
            ink_story, recipient_id)
        return_value[recipient_id] += ATTACHMENT_START + \
            str(filename) + ATTACHMENT_END + '\n'
    if next_.startswith("$meeting_attachment"):
        ink_story, filename = module.meeting_attachment(
            ink_story, recipient_id)
        return_value[recipient_id] += ATTACHMENT_START + \
            str(filename) + ATTACHMENT_END + '\n'
    if next_.startswith("$vergelijken_attachment"):
        ink_story, filename = module.vergelijken_attachment(
            ink_story, recipient_id)
        return_value[recipient_id] += ATTACHMENT_START + \
            str(filename) + ATTACHMENT_END + '\n'
    return ink_story, return_value