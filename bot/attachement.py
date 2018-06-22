ATTACHMENT_START = "$attachment,"
ATTACHMENT_END = ",attachment$"

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


def attachement_check(session_return):

    if ATTACHMENT_START in session_return:
        print("found",ATTACHMENT_START)
        session_return_edited = ""
        for line in session_return.split("\n"):
            if ATTACHMENT_START in line:
                # print("attachement",line)
                filename = line.split(ATTACHMENT_START)[1].split(ATTACHMENT_END)[0]
                session_return_edited += '<img src="/image/' + filename + '" class="widthSet" alt="pic">' + "\n"
            else:
                session_return_edited += line + "\n"

        session_return = session_return_edited
    return session_return

if __name__ == '__main__':
    text = "hello\nikbentako\n" + ATTACHMENT_START+"dir/filename"+ATTACHMENT_END+\
    "\nlastline"
    print(text)
    print(attachement_check(text))