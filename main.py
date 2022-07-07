from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://utkarsh:Password123@localhost/newdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
newdb=SQLAlchemy(app)

class Todo(newdb.Model):
    sno = newdb.Column(newdb.Integer, primary_key = True)
    title = newdb.Column(newdb.String(200), nullable = False)
    desc = newdb.Column(newdb.String(500), nullable = False)
    date_created = newdb.Column(newdb.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.sno} - {self.title}'

@app.route('/' ,methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        newdb.session.add(todo)
        newdb.session.commit()
    allTodos = Todo.query.all()
    return render_template('index.html', allTodos=allTodos)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    newdb.session.delete(todo)
    newdb.session.commit()
    return redirect('/')


@app.route('/edit/<int:sno>', methods=['GET','POST'])
def edit(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        newdb.session.add(todo)
        newdb.session.commit()
        return redirect('/')

    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

if __name__=='__main__':
    app.run(debug=True)