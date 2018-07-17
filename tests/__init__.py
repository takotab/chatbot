import requests
import random
import string

class Conversation():

    def __init__(self):
        self.conversation = []
        N = 4
        self.id_ = ''.join(random.choice(string.ascii_uppercase + string.digits)
                          for _ in range(N))

    def interact(self, msg, id_ = None):
        if id_ is None:
            id_ = self.id_

        id_ = '__id__' + id_
        url = 'http://' + 'localhost:8080'
        response = requests.get(url + '/get',params={"msg":msg + id_})
        assert response.status_code == 200 , response
        return_msg = str(response.content, 'utf-8')
        self.record(msg, return_msg)
        return return_msg

    def record(self, msg, return_msg):

        self.conversation.append("USER:" + msg)
        self.conversation.append("TINA:" + return_msg)

    def __str__(self):
        return "\n".join(self.conversation)

    def __repr__(self):
        return "\n".join(self.conversation)
