# Flask TODO_list_CSV_TXT-without-form
2nd version of data for flask TODO app still without form/CRUD. This time are data processed in csv/txt DATA_FILE

--

###### Requirements (all in python 3.10):

+ Flask (https://flask.palletsprojects.com/en/2.2.x/installation/#install-flask)
+ request
+ datetime
+ re
+ os

The inspiration was taken from the 1st Flask TODO list and should show another approach how to process data except JSON.

In second, separated cmd terminal (as described in flask installation) we get different data by requests. 

--

Allowed arguments: 
* 'od' = since, can be od='YYYY-mm-dd' or 'now' (GET)
* 'do' = until, can be do='YYYY-mm-dd' or 'now' (GET, POST only 'YYYY-mm-dd')
* 'is_done' = status of accomplishment, can be is_done='done' or 'not-done' (PUT)
* 'count' = number of tasks which should be shown, can be only integer (GET)

1. To 'GET' different data without any change: requests.get('http:///127.0.0.1:5000/..')
+ combinations possible
+ to get all tasks => http:.../todos'
+ to get all tasks for specific period => http:../todos?od=YYYY-mm-dd&do=YYYY-mm-dd'; 'od' is 'since'; 'do' is 'until'
+ to get all tasks which should be done until today => http:../todos?do=now'
+ to get all tasks which should be done after today => http:../todos?od=now'
+ to get all tasks which should be done until/after today and are (not) done => http:../todos?do/od=now&is_done=(not-done) done'
+ to define the number of tasks => http:../todos?od=YYYY-mm-dd..&count=number'
+ to get the oldest task which is not finished yet => http:../most-urgent')

2. To 'POST' a new task: requests.post('http:///127.0.0.1:5000/todo, data='taskNo,date until in form YYYY-mm-dd,description of task')

3. To 'DELETE' a task: requests.delete('http:///127.0.0.1:5000/todo/taskNo')

4. To sign task as 'finished' or back to 'in process' 'PUT' : requests.put('http:///127.0.0.1:5000/taskNo/done or not-done')

Tasks are sorted first by their date, until they should be finished, then by their alphabet and number (e.g. here task1, task2, zeppelin1 etc.)

The duplicity of tasks is possible.
