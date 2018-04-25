# todo
TODO app created for basic usage of creating task and managing them

# how to run

./manage.py makemigrations

./manage.py migrate

./manage.py runserver

# schedule a job to run on interval for checking old soft deleted records

python clock.py

# API'S 

#List of Available API'S

Task create post request

curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"title": "task name", "due_date": "2018-04-22T00:46:38", "user": "/api/user/1/"}' http://localhost:8000/api/task/

Get all task

http://127.0.0.1:8000/api/task/

Get sinlge task by id

http://127.0.0.1:8000/api/task/<task-id>

Search task by title

http://127.0.0.1:8000/api/task/?title=<task-title>

Search task by due date

http://127.0.0.1:8000/api/task/?due_date=2018-04-26

Get tasks by between two dates

http://127.0.0.1:8000/api/task/?due_date__lte=2018-04-26&postTime__gte=2018-04-26

Task Schema


http://127.0.0.1:8000/api/task//api/task/schema/
