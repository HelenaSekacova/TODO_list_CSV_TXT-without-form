from flask import Flask,request
import os
from datetime import datetime
from re import compile,split


app=Flask('my-app')

class DB():
    DATA_FILE='data'

    # check if the DATA_FILE exists or create empty one
    def file_exists(self):
        if not os.path.exists(DB.DATA_FILE):
            with open(DB.DATA_FILE, 'w') as f:
                f.write('')
    
    # open the DATA_FILE for reading, if the file hasn't existed already, creates one
    def open_file(self):
        self.file_exists()
        with open(DB.DATA_FILE, 'r') as f:
            return f.read()

    # overwrite the DATA_FILE or/and append a new row
    def write_file(self,rows,overwrite=False):
        mode= 'w' if overwrite else 'a'
        with open(DB.DATA_FILE, mode) as f:
            f.write(rows)

    # append a new row to the DATA_FILE
    def append_to_file(self,rows):
        self.write_file(rows,False)

    # overwrite the DATA_FILE
    def overwrite_file(self,rows):
        self.write_file(rows,True)

    # open the DATA_FILE, if this exists, separate its lines, sort (1st date, 2nd taskNr) and save these in DATA_FILE back; for GET and POST
    def clean_get(self):
        self.clean('\n')

    # check if data exist in the DATA_FILE for both PUT and DELETE
    def clean_del_firstPart(self,task):
        to_do_rows=len([row for row in self.cleaning_start() if row.startswith(f"{task},")])
        #print(to_do_rows)
        if to_do_rows==0:
            print(f'No {task} in DATA_FILE')
            return f'No {task} in DATA_FILE', 400

    # # open the DATA_FILE, if this exists, separate its lines, sort (1st date, 2nd taskNr) and save these; for PUT and DELETE
    def clean_delete(self,task):
        self.clean_del_firstPart(task)
        self.clean(f"{task},")

    # open a DATA_FILE and returns its lines for another action
    def cleaning_start(self):
        data=self.open_file()
        rows=data.split('\n')
        return rows

    #sort rows (1st date, 2nd taskNr) and save these in DATA_FILE back
    def cleaning_finish(self, not_deleted_rows):
        dre=compile(r'(\d+)')
        not_deleted_rows.sort(key=lambda t:(datetime.strptime(t.split(',')[1],'%Y-%m-%d'),[int(s) if s.isdigit() else s.lower() for s in split(dre,t)]))
        rows=''.join(not_deleted_rows)
        self.overwrite_file(rows)
        #print(rows)

    # clean is a complex activity which opens the DATA_FILE and orders its content(1st date, 2nd taskNr).
    def clean(self,variable): 
        not_deleted_rows=[row+'\n' for row in self.cleaning_start() if not row.startswith(variable) and row!='']
        self.cleaning_finish(not_deleted_rows)   

    # after check if the task exists in the DATA_FILE, removes the 'is_done' and replaces this with the user's input
    def put(self, task,set_done):
        self.clean_del_firstPart(task)
        set_variable=f",{set_done}"
        not_deleted_rows=[]
        for row in self.cleaning_start():
            if row!='' and row!='\n':
                if row.startswith(f"{task},"):
                    #print(task)
                    row=row.split(',')
                    #print(row)
                    del(row[-1])
                    #print(row)
                    row=','.join(row)+set_variable
                not_deleted_rows.append(row+'\n')
        self.cleaning_finish(not_deleted_rows)
        
    

db=DB()

# get through 'todos'
@app.route('/todos')
    # 0. combinations possible
    # 1. get all tasks => http:.../todos'
    # 2. get all tasks for specific period => http:../todos?od=YYYY-mm-dd&do=YYYY-mm-dd'; 'od' is 'since'; 'do' is 'until'
    # 3. get all tasks which should be done until today => http:../todos?do=now'
    # 4. get all tasks which should be done after today => http:../todos?od=now'
    # 5. get all tasks which should be done until/after today and are (not) done => http:../todos?do/od=now&is_done=(not-done) done'
    # 6. define the number of tasks => http:../todos?od=YYYY-mm-dd..&count=number'
def get_todos():
    # args => to get argument/s which is typed after 'http:.../todos?do=YYYY-mm-dd&od=YYYY-mm-dd&...'
    args=request.args.to_dict()
    allowed_args=['od','do','count','is_done']
    for key in args.keys():
        if key not in allowed_args:
            print(f'"{key}" is not valid argument.')
            return f'"{key}" is not valid argument.',400

    if request.args.get('od')==None:
        od=datetime.strptime('0001-01-01', '%Y-%m-%d')
        #print(od)
        #return 'ok'
    elif request.args.get('od')=='now':
        today=datetime.today().strftime('%Y-%m-%d')
        od=datetime.strptime(today, '%Y-%m-%d')
        #print(od)
        #return 'ok'
    elif request.args.get('od')!='now':
        try:
            od=datetime.strptime(request.args.get('od'), '%Y-%m-%d')
        except ValueError:
            print(f"{request.args.get('od')} is not valid date.")
            return f"{request.args.get('od')} is not valid date.",400
        else:
            od=od
            #return 'Something is wrong'

    if request.args.get('count')==None:
        count=None
    else:
        try:
            count=int(request.args.get('count'))
        except ValueError:
            print(f"{request.args.get('count')} is not integer.")
            return f"{request.args.get('count')} is not integer.",400
        else:
            count=count
            #print(count)
        
    if request.args.get('do')==None:
        do=datetime.strptime('9999-12-12', '%Y-%m-%d')
        #print(do)
        #return 'ok'
    elif request.args.get('do')=='now':
        today=datetime.today().strftime('%Y-%m-%d')
        do=datetime.strptime(today, '%Y-%m-%d')
        #print(do)
        #return 'ok'
    elif request.args.get('do')!='now':
        try:
            do=datetime.strptime(request.args.get('do'), '%Y-%m-%d')
        except ValueError:
            print(f"{request.args.get('do')} is not valid date.")
            return f"{request.args.get('do')} is not valid date.",400
        else:
            do=do
            #return 'Something is wrong'
    #print(do)

    if request.args.get('is_done')==None:
        is_done=None
        #print(is_done)
        #return 'ok'
    elif request.args.get('is_done')=='done':
        is_done='done'
        #print(is_done)
        #return 'ok'
    elif request.args.get('is_done')=='not-done':
        is_done='not-done'
        #print(is_done)
        #return 'ok'
    else:
        print(f"{request.args.get('is_done')} is not valid for is_done.")
        return f"{request.args.get('is_done')} is not valid for is_done.",400
    #print(is_done)

    # for no arguments => resp=requests.get('http://127.0.0.1:5000/todos')
    if args=={}:
        #print(args)
        #print(type(args))
        rows=db.cleaning_start()
        urgent=[]
        for row in rows:
            if row!='' and row!='\n':
                datum=datetime.strptime(row.split(',')[1],'%Y-%m-%d')
                if od<datum<do:
                    urgent.append(row+'\n')
        #print(urgent)
        dre=compile(r'(\d+)')
        urgent.sort(key=lambda t:(datetime.strptime(t.split(',')[1],'%Y-%m-%d'),[int(s) if s.isdigit() else s.lower() for s in split(dre,t)]))
        result=''.join(urgent)
        print(result)
        return result
    else:
        #print(args)
        rows=db.cleaning_start()
        urgent=[]
        for row in rows:
            if row!='' and row!='\n' and is_done==None:
                datum=datetime.strptime(row.split(',')[1],'%Y-%m-%d')
                if od<datum<do:
                    urgent.append(row+'\n')
            elif row!='' and row!='\n' and row.split(',')[-1]==is_done:
                datum=datetime.strptime(row.split(',')[1],'%Y-%m-%d')
                if od<datum<do:
                    urgent.append(row+'\n')
        dre=compile(r'(\d+)')
        urgent.sort(key=lambda t:(datetime.strptime(t.split(',')[1],'%Y-%m-%d'),[int(s) if s.isdigit() else s.lower() for s in split(dre,t)]))
        result=''.join(urgent[:count])
        print(result)
        return result
    
# for a task which should be done as a first of all => the oldest one which has not done yet
# resp=requests.get('http://127.0.0.1:5000/most-urgent')
@app.route('/most-urgent')
def urgent():
    urgent=[]
    dates=[]
    for row in db.cleaning_start():
        if row.split(',')[-1]=='not-done' and row!='' and row!='\n':
            datum=datetime.strptime(row.split(',')[1],'%Y-%m-%d')
            urgent.append(row)
            dates.append(datum)
    try:
        too_late=(min(dates)).strftime('%Y-%m-%d')
    except ValueError:
        print('No data')
        return 'No data',400
    else:
        all_urgent=[]
        for row in urgent:
            if row.split(',')[1]==too_late and row!='' and row!='\n':
                all_urgent.append(row+'\n')
        result=''.join(all_urgent)
        print(result)
        return result
#resp=requests.post('http://127.0.0.1:5000/todo', data='taskNr,YYYY-mm-dd,activity');
# taskNr =>'task' can be any character, Nr should be integer
# YYYY-mm-dd => is for 'do' until when should be task finished
# activity => description of task
@app.route('/todo',methods=['POST'])
def post_todo():
    data=request.data.decode()
    if len(data.split(','))!=3:
        print('Check your task: data="taskNr, YYYY-mm-dd, description of task"')
        return 'Check your task: data="taskNr, YYYY-mm-dd, description of task"',400
    else:
        try:
            datetime.strptime(data.split(',')[1],'%Y-%m-%d')
        except ValueError:
            print('No valid date')
            return 'No valid date', 400
        else:
            data=''.join(data)+',not-done'+'\n' 
            db.append_to_file(data)
            db.clean_get()
            return 'ok'

#resp=requests.delete('http://127.0.0.1:5000/todo/taskNr')
@app.route('/todo/<task>',methods=['DELETE'])
def delete_todo(task):
    task=task
    db.clean_delete(task)
    return 'ok'

# define if task is completed or not. Default value by POSTing is 'not-done'
#resp=requests.put('http://127.0.0.1:5000/taskNr/done') (or not-done')
@app.route('/<task>/<set_done>',methods=['PUT'])
def set_put(task,set_done):
    task=task
    set_done=set_done
    db.put(task,set_done)
    return 'ok'   

# only for test if the app works online
@app.route('/')
def hello():
    return 'Funguji'



if __name__=='__main__':
    app.run(debug=True)
