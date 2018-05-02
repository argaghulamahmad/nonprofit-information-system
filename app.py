import os
import psycopg2
from flask import Flask, render_template, session, request, flash
import urllib.parse
from os.path import exists
from os import makedirs

# connect for deployed application at heroku
# url = urlparse.urlparse(os.environ.get('DATABASE_URL'))
# db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
# schema = "schema.sql"
# conn = psycopg2.connect(db)

# connect to local database
# change this variables according your local database
dbname = 'argaghulam'  # database name
username = 'postgres'  # username
password = 'postgres'  # password

conn_string = "host='localhost' dbname=%s user=%s password=%s " % (dbname, username, password)
conn = psycopg2.connect(conn_string)

cur = conn.cursor()

app = Flask(__name__)


# home controller by Arga G. A.
# is user have logged in? redirect to correct feature
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return render_template('dashboard.html', userName=session['name'])


# login controller by Arga G. A.
# redirect to login page
@app.route('/login')
def loginPage():
    return render_template('login.html')


# login with post method controller by Arga G. A.
# is username exists? is passwords is correct? redirect to correct feature
# mark user have logged in
@app.route('/login', methods=['POST'])
def login():
    try:
        requestEmail = request.form['email']
        requestPassword = request.form['password']

        cur.execute("""select * from sion.pengguna where email = {}""".format("'" + requestEmail + "'"))
        userObj = cur.fetchone()
        correctPassword = userObj[1]
        requestName = userObj[2]

        print(requestName + " " + requestEmail + " " + requestPassword + " " + correctPassword)
        if requestPassword == correctPassword:
            session['email'] = requestEmail
            session['name'] = requestName
            session['logged_in'] = True
            print("Login success!")
        else:
            print("Login failed!")
            flash('wrong password!')
        return home()
    except Exception as e:
        print("Ada kesalahan pada method getUsersEmail(), " + e)
        return "Ada kesalahan pada fungsi getUsersEmail."


# logout controller by Arga G. A.
# mark user have logged out
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


# users controller by Arga G. A.
# this is template controller
# retrieve all users email
@app.route('/users')
def getUsersEmail():
    try:
        cur.execute("""SELECT * from sion.pengguna""")
        rows = cur.fetchall()
        my_list = []
        for row in rows:
            my_list.append(row[0])

        return render_template('users.html', results=my_list)
    except Exception as e:
        print("Ada kesalahan pada method getUsersEmail(), " + e)
        return "Ada kesalahan pada fungsi getUsersEmail."


# main method to run the web server
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run()
