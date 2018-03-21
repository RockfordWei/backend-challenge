import os
import json
import unittest
from adachat import ChatManager

class TestChat(unittest.TestCase):
    
    __chatman = None
    
    def setUp(self):
        try: 
            os.remove('/tmp/chat.db')
        except OSError:
            pass
        self.__chatman = ChatManager()
        
    def tearDown(self):
        self.__chatman = None
        try: 
            os.remove('/tmp/chat.db')
        except OSError:
            pass

    def testAppend(self):
        id = ChatManager.allocate_conversation_id()
        json_string = '''
        {
            "sender": "anson",
            "conversation_id": "%s",
            "message": "I'm a teapot"
        }
        ''' % (id,)
        self.__chatman.append(json_string)
        resp = self.__chatman.query(id)
        self.assertTrue(resp)
        r = json.loads(resp)
        self.assertEqual(r['id'], id)
        msg = r['messages']
        self.assertEqual(len(msg), 1)
        m = msg[0]
        self.assertEqual(m['sender'], 'anson')
        self.assertEqual(m['message'], "I'm a teapot")

if __name__ == '__main__':
    unittest.main()
