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
dbname = 'aldihilman'  # database name
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
        return render_template('dashboard.html', userName=session['name'], userRole=session['role'])


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

        if userObj:
            correctPassword = userObj[1]
            requestName = userObj[2]

            print(requestName + " " + requestEmail + " " + requestPassword + " " + correctPassword)
            if requestPassword == correctPassword:
                session['email'] = requestEmail
                session['name'] = requestName
                userRole = getUserRole(requestEmail)
                session['role'] = userRole
                session['{}'.format(userRole)] = True
                session['logged_in'] = True
                print("Login success!")
            else:
                print("Login failed, wrong password!")
                flash('wrong password!')
            return home()
        else:
            print("Pengguna tidak ada!")
            flash("User doesnt exist!")
            return loginPage()
    except Exception as e:
        print("Ada kesalahan pada method getUsersEmail(), " + e)
        return "Ada kesalahan pada fungsi getUsersEmail."


# logout controller by Arga G. A.
# mark user have logged out
@app.route("/logout")
def logout():
    session.clear()
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


def getUserRole(requestEmail):
    try:
        cur.execute(
            """select * from sion.pengguna, sion.donatur where sion.pengguna.email = sion.donatur.email and sion.pengguna.email = {}""".format(
                "'" + requestEmail + "'"))
        isDonatur = cur.fetchall
        cur.execute(
            """select * from sion.pengguna, sion.relawan where sion.pengguna.email = sion.relawan.email and sion.pengguna.email = {}""".format(
                "'" + requestEmail + "'"))
        isRelawan = cur.fetchall
        cur.execute(
            """select * from sion.pengguna, sion.sponsor where pengguna.email = sion.sponsor.email and sion.pengguna.email = {}""".format(
                "'" + requestEmail + "'"))
        isSponsor = cur.fetchall
        cur.execute(
            """select * from sion.pengguna, sion.pengurus_organisasi where sion.pengguna.email = sion.pengurus_organisasi.email and pengguna.email = {}""".format(
                "'" + requestEmail + "'"))
        isPengurusOrganisasi = cur.fetchall

        if isRelawan:
            print("relawan")
            return "relawan"
        elif isDonatur:
            print("donatur")
            return "donatur"
        elif isSponsor:
            print("sponsor")
            return "sponsor"
        elif isPengurusOrganisasi:
            print("pengurus organisasi")
            return "pengurus organisasi"
        else:
            print("Error: tidak terdaftar pada role manapun")
            return "none"
    except Exception as e:
        print("Ada kesalahan pada method getUsersEmail(), " + e)
        return "Ada kesalahan pada fungsi getUsersEmail."

# users controller by Aldi Hilman Ramadhani
# this is template controller
# retrieve all users email
@app.route('/organization')
def view_organization_list():
    cur.execute("""select email_organisasi, website, nama, status_verifikasi from sion.organisasi""")
    rows = cur.fetchall()
    organizations = []
    for row in rows:
        
        organization = {
            'email' : row[0],
            'website' : row[1],
            'nama' : row[2],
            'status_verifikasi' : row[3],
        }
        
        organizations.append(organization)

    return render_template(
        'organization_list.html',
        userName=session['name'],
        userRole=session['role'],
        organizations=organizations
    )

@app.route('/organization/<email>')
def view_organization_profle(email):
    organization_email = email
    
    rows = cur.execute(
            """select * 
            from sion.organisasi 
            where email_organisasi={}""".format(
            "'" + organization_email + "'"))
    biodata_organisasi = cur.fetchone()

    rows = cur.execute(
            """select U.email, U.nama, U.alamat_lengkap
            from sion.pengguna U, sion.pengurus_organisasi P, sion.organisasi O
            where O.email_organisasi={}
            and P.organisasi=O.email_organisasi
            and U.email=P.email""".format(
            "'" + organization_email + "'"))
    pengurus_organisasi = cur.fetchall()

    rows = cur.execute(
            """select *
            from sion.donatur_organisasi
            where organisasi={}""".format(
            "'" + organization_email + "'"))
    donasi_donatur = cur.fetchall()

    rows = cur.execute(
            """select *
            from sion.sponsor_organisasi
            where organisasi={}""".format(
            "'" + organization_email + "'"))
    donasi_sponsor = cur.fetchall()

    rows = cur.execute(
            """select sum(S.nominal)+sum(D.nominal)
            from sion.sponsor_organisasi S,
            sion.donatur_organisasi D
            where S.organisasi={}
            and D.organisasi={}""".format(
            "'" + organization_email + "'",
            "'" + organization_email + "'"))
    total_donasi = cur.fetchone()

    return render_template(
        'organization_profile.html',
        userName=session['name'],
        userRole=session['role'],
        biodata_organisasi=biodata_organisasi,
        pengurus_organisasi=pengurus_organisasi,
        donasi_donatur=donasi_donatur,
        donasi_sponsor=donasi_sponsor,
        total_donasi=total_donasi
    )


# main method to run the web server
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run()
