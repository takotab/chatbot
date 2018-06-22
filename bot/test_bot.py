from . import attachement

def test():
    text = "hello\nikbentako\n" + attachement.ATTACHMENT_START+\
    "dir/filename"+attachement.ATTACHMENT_END+\
    "\nlastline"

    assert attachement.attachement_check(text).contains("<img src=") == True