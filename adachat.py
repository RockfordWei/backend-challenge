# Ada Support Backend Developer Challenge
# Solution by Rocky Wei March 21, 2018

import json
import re
import sqlite3
import uuid

class ChatManager:
    # Chat Manager Class
    # basic functions: 
    # - open a sqlite3 database for data logging
    # - implement append(json) for logging a new chat message
    # - implement query(conversation_id) for retrieving the associated chat history
    # - other utilites, such as unified timestamp and uuid for testing purposes
    
    # sqlite database connection
    __db = None
    
    # precompiled pattern for sender id validation
    __pattern_sender = None
    
    # precompiled pattern for conversation id validation 
    __pattern_conversation = None
    
    def __init__(self, location='/tmp/chat.db'):
        # constructor
        # Args: location - sqlite database path
        # Yields: sqlite3 errors
        
        # sender id must be an alphabetic/number mixture in max 32 characters 
        self.__pattern_sender = re.compile('^[a-zA-Z0-9]{1,32}$')
        
        # conversation must be a hex format of uuid4
        self.__pattern_conversation = re.compile('^[a-f0-9]{32}$')
        self.__db = sqlite3.connect(location)
        cursor = self.__db.cursor()
        
        
        # in such a context, a user should not be able to log more than one 
        # messages in the same millisecond
        # so primary key(created, conversation, sender) could be a good idea
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS history(
            created VARCHAR(32),
            conversation VARCHAR(32),
            sender VARCHAR(32),
            message VARCHAR(256),
            PRIMARY KEY(created, conversation, sender)
        )
        ''')
        self.__db.commit()
        cursor.close()
        
    def __del__(self):
        self.__db.close()
        
    def now(self):
        # for testing purposes, return a unified utc time from the database
        cursor = self.__db.cursor()
        cursor.execute("SELECT strftime('%Y-%m-%dT%H:%M:%S.%fZ', 'now')")
        row = cursor.fetchone()
        cursor.close()
        return row[0]
    
    @staticmethod
    def allocate_conversation_id():
        # for testing purposes, return a sample of uuid4
        return uuid.uuid4().hex
    
    def append(self, json_string):
        # parse a json input and log the content into database, for example
        # {
        # "sender": "anson",
        # "conversation_id": "6e0e189f62ab4ea386bb375e07813d03",
        # "message": "I'm a teapot"
        # }
        # If success, the method simply just won't yield anything wrong
        x = json.loads(json_string)
        conversation = x['conversation_id']
        sender = x['sender']
        message = x['message']
        
        # validate conversation id, must be a hex presentation of uuid4
        assert self.__pattern_conversation.match(conversation), ValueError('conversation id must be a valid uuid4')
        assert int(conversation, 16), ValueError('conversation id must be a valid uuid4')
        
        # validate user id
        assert self.__pattern_sender.match(sender), ValueError('invalid sender id')
        
        # trim the message is a minimal sanitization,
        # production server should at least avoid sql and other script injection
        message = message.strip()
        size = len(message)
        assert size in range(1, 256), ValueError('invalide message size')
        cursor = self.__db.cursor()
        sql = """
        INSERT INTO history(created, conversation, sender, message) 
        VALUES(strftime('%Y-%m-%dT%H:%M:%S.%fZ', 'now'), ?, ?, ?)
        """
        cursor = self.__db.cursor()
        cursor.execute(sql, (conversation, sender, message,))
        self.__db.commit()
        cursor.close()
                
    def query(self, conversation): 
        # return historical record by a certain conversation_id
        # for example:
        # {"messages": [{"message": "I'm a teapot", "created": "2018-03-21T18:21:17.17.611Z", "sender": "anson"}],
        #  "id": "6e0e189f62ab4ea386bb375e07813d03"}
        assert self.__pattern_conversation.match(conversation), ValueError('conversation id must be a valid uuid4')
        assert int(conversation, 16), ValueError('conversation id must be a valid uuid4')
        
        cursor = self.__db.cursor()
        cursor.execute('SELECT sender, message, created FROM history WHERE conversation = ? ORDER BY created', (conversation,))
        messages = []
        for row in cursor:
            m = {'sender': row[0], 'message': row[1], 'created': row[2]}
            messages.append(m)
        
        history = {'id': conversation, 'messages': messages}
        return json.dumps(history)
