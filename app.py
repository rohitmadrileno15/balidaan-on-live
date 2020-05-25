from flask import Flask,request,render_template,flash
from flask_sqlalchemy import SQLAlchemy
import time
import re
from flask_wtf import FlaskForm
from wtforms import validators, StringField , SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = '450933c08c5ab75e79619102eddf47dee813a9d6'



class ContactForm(FlaskForm):

    language = SelectField('Year list', validators = [DataRequired()] ,choices = [("2000", '2000-date'),
      ("1970", '1970-1999'),("1947", '1947-1969')])
    submit = SubmitField("Get")

class SearchForm(FlaskForm):
    name = StringField('Name' , validators = [DataRequired()])

    submit = SubmitField('Search')


@app.route('/')
def hello_world():
    conn = sqlite3.connect("test.db")

    cursor = conn.cursor()

    cursor.execute('''SELECT * from emp''')

    result = cursor.fetchall();

    conn.commit()

    conn.close()
    arr = result
    return render_template('index.html', posts = arr)


@app.route('/find', methods = ['GET', 'POST'])
def contact():
    result_date = None
    form = ContactForm()
    conn = sqlite3.connect("test.db")

    cursor = conn.cursor()

    if (form.validate_on_submit() ):
        date_data = (form.language.data)
        print(date_data)

        if(date_data=='2000'):
            cursor.execute('''SELECT * from emp WHERE year BETWEEN 2000 AND 2020 ''')

            result_date = cursor.fetchall();

            conn.commit()
        if(date_data=='1970'):
            cursor.execute('''SELECT * from emp WHERE year BETWEEN 1970 AND 1999 ''')

            result_date = cursor.fetchall();

            conn.commit()
        if(date_data=='1947'):
            cursor.execute('''SELECT * from emp WHERE year BETWEEN 1944 AND 1969 ''')

            result_date = cursor.fetchall();

            conn.commit()

        conn.close()
        return render_template('result_data.html', posts = result_date)

    return render_template('contact.html', form = form)


@app.route('/search' , methods=['GET', 'POST'])
def search():
    n= None
    find_ = None

    form = SearchForm()
    if (form.validate_on_submit() ):
        name = form.name.data
        print(name)

        conn = sqlite3.connect("test.db")

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM emp WHERE name LIKE '%{}%' ".format(name))

        result = cursor.fetchall();

        conn.commit()
        print(result)
        form.name.data = ""

        conn.close()

        return render_template('search.html',form = form, posts = result, alert=n)





    return render_template('search.html',form = form, posts = find_, alert=n)



if __name__ == '__main__':
    app.run(debug= True)
