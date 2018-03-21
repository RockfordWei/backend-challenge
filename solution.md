
#Ada Support Backend Developer Challenge
##Candidate Solution - Python


## Sources

File Name|Description
---------|-----------
README.md|Content of the Challenge
`__init__.py`|Empty place holder as python required
`__main__.py`|Demo server scripts
adachat.py|Solution class
run.sh|bash script to boot the demo server
solution.md|you are reading this file
test.py|unit test for the solution class
test.sh|bash script to wrap up the whole tests

## Prerequisites

Python 3.5.2+

## Build & Run from Source

Once cloned, simply run `python3 .` should immediately bring up a web server on 8181, assuming your system is a linux or mac, with at least a `/tmp` folder. 

### Unit Test

`python3 test.py` may perform a simple unit test for demo purposes.

## Alternative Run via Docker

Assuming docker is running, then `./run.sh` should download my personal docker repo `rockywei/python:3` (which is actually only `ubuntu:16.04` with `apt-get update -y && apt-get upgrade -y && apt-get install -y python3`):

```
$ ./run.sh
./run.sh 
2018-03-21T21:03:09.09.741Z Server 8181 starts
```

Control-C may stop this http server instance on 8181

### Perform Test via Docker

`./test.sh` may run a fuller test by jumping out of the python's own sandbox:

```
$ ./test.sh 

Step #1: run unit test first
.
----------------------------------------------------------------------
Ran 1 test in 0.022s

OK

Step #2: start server on 8181

Step #3: wait for server boot

Step #4: try getting an id

Step #5: try posting
{"error": 0}
{"error": 0}

Step #6: try fetching chat history of 562bda4bff5c4f2ca76d8fdce8ae80fe
{"messages": [{"sender": "anson", "created": "2018-03-21T21:06:48.48.375Z", "message": "I am a teapot"}, {"sender": "megan", "created": "2018-03-21T21:06:48.48.408Z", "message": "I am a cup"}], "id": "562bda4bff5c4f2ca76d8fdce8ae80fe"}
Step #7: clean up
d0d0d746b4db
```

## Documentation

### Basic Design

The solution is implementing a `ChatManager()` class to control the incoming messages and conversation history as well. Then a `http.server` wraps it up to finish the routing.

**Features**:

- Applied regular expressions to perform the input string validation.
- SQLite3 integration.
- Essential message content injection prevention.
- Primary Key On (conversation_id, created, sender)
- JSON returns track info when error happens.
- Extra API for generate uuid4 testing string in a hex form.
- Using database UTC time stamp to avoid time differences on application servers.


### Class ChatManager()

API| constructor
---|-----------
Parameters|location='/tmp/db'
Yields|sqlite3 error
Returns|ChatManager instance
Description|initialize a chat manager instance and a sqlite3 connection as well
Example|`cm = ChatManager(location='/path/to/myfile.db')`

API| `now()`
---|-----------
Parameters|N/A
Yields|sqlite3 error
Returns|UTC Time Stamp
Description|For some reasons, if the database server was an independent server, then it would be a good idea to use the database server clock instead of locally.
Example|`utf = cm.now()`

API| `allocate_conversation_id()`
---|-----------
Parameters|N/A
Yields|uuid exceptions
Returns|a hex string of uuid4
Description|a static method to generate a unified conversation id
Example|`conversation_id = ChatManager.allocate_conversation_id()` would likely generate something like `562bda4bff5c4f2ca76d8fdce8ae80fe`

API| `append(json_string)`
---|-----------
Parameters|json_string
Yields|ValueError for invalid `conversation_id` or `sender`, or unacceptable `message coding`
Returns|N/A
Description|append a json message post into chat history
Example|`cm.append(json)` (See Challenge JSON post for detail)

API| `query(conversation)`
---|-----------
Parameters|conversation id
Yields|ValueError for invalid `conversation_id`, or sqlite3 errors
Returns|json string for the conversation history
Description|retrieving conversations by the input id
Example|`json_ret = cm.query(id)` (See Challenge JSON GET return for detail)

## Missing Parts

A complete testing script should be added and cover all possible inputs, such as script (python/javascript/sql) injection, overflow DDoS, conversation id stolen and abuse, same users with different ip in the same window time  - however, as illustrated in the challenge, authentication & security issue is out of the range.

## Go Further

Honestly, 8 hours would not be possible to fully implement all considerations, such as:

Challenge|Solution
--------|---------
Chat record exceeds 1 million|1. Split table by date, typically expired data would be archived by year (or month); 2. Replacing database to HIVE (relational), or HBASE (key-value)
Message Search|For relational database, lucern with Sphinx could be a good choice for full text searching, however, HIVE/HBASE is still highly recommended. 
Message Undo|Snapchat? Extra flags should put into the table to mark a message deletion
Multimedia Message|Audio/Video/File/Snippet/Poll ... everything in the Slack may be also required in such an app. So JSON would be helpful
WebSocket/WebRTC/Online Gaming|http 1.1 is strong enough, but other interactive chat may require a lot callbacks. Web Socket is the most recommended backboned with Apache Kafka/MQTT, otherwise the token management would be highly sticky.
AI/Bot|TensorFlow is good at word2vec, LSTM and other machine learning models. Source archive of twitter may be a good source to train you bot, however, to make your bot smarter, there would be much more variables to introduce such as text to audio/picture/video, and emojis as well.

## Even Further?

Python is powerful, however, it is not the only solution for this case, please check my personal repository [anagram in different frameworks](https://github.com/RockfordWei/anagram.git) for other possible options, such as NodeJS/Java/Swift/PHP. All languages have pros and cons, I have a benchmark for all of them and would like to share if request.


## Contributor

[Rocky's linked-in profile](https://www.linkedin.com/in/rockfordwei/)

[Rocky's github](https://github.com/RockfordWei)


