from flask import current_app


def attachement_check(session_return):
    ATTACHMENT_END = current_app.config["ATTACHMENT_END"]
    ATTACHMENT_START = current_app.config["ATTACHMENT_START"]

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

    ATTACHMENT_END = current_app.config["ATTACHMENT_END"]
    ATTACHMENT_START = current_app.config["ATTACHMENT_START"]
    
    text = "hello\nikbentako\n" + ATTACHMENT_START+"dir/filename"+ATTACHMENT_END+\
    "\nlastline"
    print(text)
    print(attachement_check(text))