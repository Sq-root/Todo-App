
from flask import Flask , render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#-----------------------------------------
#  Table Name : Todo
#  Col: sno , title, desc, date_created, status
#-----------------------------------------
class Todo(db.Model):
    sno = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(200) , nullable = False)
    desc = db.Column(db.String(500) , nullable = False)
    date_created = db.Column(db.Date , default = datetime.utcnow)
    status = db.Column(db.Integer, default= 0)
    

#-----------------------------------------
#               Completed Task List
#-----------------------------------------
@app.route("/completed_task",methods=['GET','POST'])
def completed_task():
    title ="Task History"
    allTodo = Todo.query.filter_by(status =1)
    return render_template('display_task.html', allTodo = allTodo,title=title )


#-----------------------------------------
#               Pending Task List
#-----------------------------------------
@app.route("/incomplete_task",methods=['GET','POST'])
def incomplete_task():
    title ="Pending Task"
    allTodo = Todo.query.filter_by(status = 1)
    print("table: ", allTodo)
    return render_template('display_task.html', allTodo = allTodo, title=title )


#-----------------------------------------
#               Home Page
#-----------------------------------------
@app.route("/",methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        title =  request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit() 
    allTodo = Todo.query.all()
    return render_template('index.html' , allTodo = allTodo)



#-----------------------------------------
#               Delete List
#-----------------------------------------
@app.route("/delete/<int:sno>")
def delete(sno):
    """ recieved post requests for entry Delete Task """
    todo = Todo.query.filter_by(sno =sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")



#-----------------------------------------
#               Update List
#-----------------------------------------
@app.route("/update/<int:sno>", methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        """ recieved post requests for entry update Task"""
        title =  request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno =sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    todo = Todo.query.filter_by(sno =sno).first()
    return render_template('update.html' , todo = todo)

#-----------------------------------------
#               Update Status of Task
#-----------------------------------------
@app.route("/status/<int:sno>", methods=['GET','POST'])
def status_update(sno):
    if request.method == 'POST':
        """ recieved post requests for status update of task"""
        todo = Todo.query.filter_by(sno =sno).first()
        if todo.status == 1:
            todo.status=0
        else:
            todo.status=1
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    allTodo = Todo.query.all()
    return render_template('index.html' , allTodo = allTodo)


if __name__ == "__main__":
    app.run(debug = True,port = 8000) 
    