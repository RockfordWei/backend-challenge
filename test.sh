printf "\nStep #1: run unit test first\n"
docker run  -v $PWD:/home -v /tmp:/tmp -w /home rockywei/python:3 /bin/bash -c "python3 test.py"
printf "\nStep #2: start server on 8181\n"
docker run -v $PWD:/home -v /tmp:/tmp -w /home -p 8181:8181 rockywei/python:3 /bin/bash -c "python3 ." &
printf "\nStep #3: wait for server boot\n"
sleep 3
printf "\nStep #4: try getting an id\n"
conversation_id=$(curl -s http://localhost:8181| awk '{gsub(/"/, "", $2); gsub(/}/, "", $2); print $2}')
printf "\nStep #5: try posting\n"
curl -X POST -d "{\"sender\": \"anson\",\"conversation_id\": \"$conversation_id\",\"message\": \"I am a teapot\"}" \
http://localhost:8181/messages/ && echo
curl -X POST -d "{\"sender\": \"megan\",\"conversation_id\": \"$conversation_id\",\"message\": \"I am a cup\"}" \
http://localhost:8181/messages/ && echo
printf "\nStep #6: try fetching chat history of $conversation_id\n"
curl "http://localhost:8181/conversations/$conversation_id"
printf "\nStep #7: clean up\n"
docker kill $(docker ps |grep rockywei|awk '{print $1}')
