import os

import psycopg2
from flask import Flask, render_template, session, request

# import urllib.parse
# from os.path import exists
# from os import makedirs

# connect for deployed application at heroku
# url = urlparse.urlparse(os.environ.get('DATABASE_URL'))
# db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
# schema = "schema.sql"
# conn = psycopg2.connect(db)

# connect to local database
# change this variables according your local database
dbname = 'db081'  # database name
username = 'db081'  # username
password = 'saiT8Noo'  # password

conn_string = "host='dbpg.cs.ui.ac.id' dbname=%s user=%s password=%s " % (dbname, username, password)
conn = psycopg2.connect(conn_string)
conn.autocommit = True

cur = conn.cursor()

app = Flask(__name__)


# home controller by Arga G. A.
# is user have logged in? redirect to correct feature
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return dashboard(recentlyRegistered=False)


# dashboard controller by Arga G. A.
# provide dashboard page
@app.route('/dashboard', defaults={'recentlyRegistered': False})
def dashboard(recentlyRegistered):
    if session.get('logged_in'):
        return render_template('dashboard.html', userName=session['name'], userRole=session['role'],
                               recentlyRegistered=recentlyRegistered)
    else:
        return loginPage(wrongPassword=False, notExist=False)


# login controller by Arga G. A.
# redirect to login page
@app.route('/login', defaults={'wrongPassword': False, 'notExist': False})
def loginPage(wrongPassword, notExist):
    return render_template('login.html', wrongPassword=wrongPassword, notExist=notExist)


# login with post method controller by Arga G. A.
# is username exists? is passwords is correct? redirect to correct feature
# mark user have logged in
@app.route('/login', methods=['POST'])
def login():
    try:
        requestEmail = request.form["email"]
        requestPassword = request.form["password"]

        cur.execute("""select * from sion.pengguna where email = {}""".format("'" + requestEmail + "'"))
        userObj = cur.fetchone()

        if userObj:
            correctPassword = userObj[1]
            requestName = userObj[2]

            # print(requestName + " " + requestEmail + " " + requestPassword + " " + correctPassword)
            if requestPassword == correctPassword:
                session['email'] = requestEmail
                session['name'] = requestName
                userRole = getUserRole(requestEmail)
                session['role'] = userRole
                session['{}'.format(userRole)] = True
                session['logged_in'] = True
                print("Login success!")
                return dashboard(recentlyRegistered=False)
            else:
                print("Login failed, wrong password!")
                return loginPage(wrongPassword=True, notExist=False)
        else:
            print("Pengguna tidak ada!")
            return loginPage(wrongPassword=False, notExist=True)
    except Exception as e:
        print(str(e))
        return "Ada kesalahan pada sistem"


# logout controller by Arga G. A.
# mark user have logged out
@app.route("/logout")
def logout():
    session.clear()
    session['logged_in'] = False
    return home()


# users emails controller by Arga G. A.
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
        print(str(e))
        return "Ada kesalahan pada sistem."

# get user role controller by Arga G. A.
# determine role of user by using email
# retrieve user role
def getUserRole(requestEmail):
    try:
        cur.execute(
            """select * from sion.pengguna, sion.donatur where sion.pengguna.email = sion.donatur.email and sion.pengguna.email = {}""".format(
                "'" + requestEmail + "'"))
        isDonatur = cur.fetchall()
        print(isDonatur)
        cur.execute(
            """select * from sion.pengguna, sion.relawan where sion.pengguna.email = sion.relawan.email and sion.pengguna.email = {}""".format(
                "'" + requestEmail + "'"))
        isRelawan = cur.fetchall()
        print(isRelawan)
        cur.execute(
            """select * from sion.pengguna, sion.sponsor where pengguna.email = sion.sponsor.email and sion.pengguna.email = {}""".format(
                "'" + requestEmail + "'"))
        isSponsor = cur.fetchall()
        print(isSponsor)
        cur.execute(
            """select * from sion.pengguna, sion.pengurus_organisasi where sion.pengguna.email = sion.pengurus_organisasi.email and pengguna.email = {}""".format(
                "'" + requestEmail + "'"))
        isPengurusOrganisasi = cur.fetchall()
        print(isPengurusOrganisasi)

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
        print(str(e))
        return "Ada kesalahan pada sistem."

#created by Bram
def getInformationRelawan(requestEmail):
    cur.execute(
        """select keahlian from sion.KEAHLIAN_RELAWAN where sion.KEAHLIAN_RELAWAN.email = {}""".format(
            "'" + requestEmail + "'"))
    session['keahlian'] = cur.fetchall()
    cur.execute(
        """select nama from sion.PENGGUNA where sion.PENGGUNA.email = {}""".format(
            "'" + requestEmail + "'"))
    session['nama'] = cur.fetchone()[0]
    cur.execute(
        """select alamat_lengkap from sion.PENGGUNA where sion.PENGGUNA.email = {}""".format(
            "'" + requestEmail + "'"))
    session['alamat'] = cur.fetchone()[0]
    cur.execute(
        """select tanggal_lahir from sion.RELAWAN where sion.RELAWAN.email = {}""".format(
            "'" + requestEmail + "'"))
    session['tanggal_lahir'] = cur.fetchone()[0]
    cur.execute(
        """select no_hp from sion.RELAWAN where sion.RELAWAN.email = {}""".format(
            "'" + requestEmail + "'"))
    session['no_hp'] = cur.fetchone()[0]

#created by Bram
def getInformationDonatur(requestEmail):
    cur.execute(
        """select nama from sion.PENGGUNA where sion.PENGGUNA.email = {}""".format(
            "'" + requestEmail + "'"))
    session['nama'] = cur.fetchone()[0]
    cur.execute(
        """select alamat_lengkap from sion.PENGGUNA where sion.PENGGUNA.email = {}""".format(
            "'" + requestEmail + "'"))
    session['alamat'] = cur.fetchone()[0]
    cur.execute(
        """select saldo from sion.DONATUR where sion.DONATUR.email = {}""".format(
            "'" + requestEmail + "'"))
    session['saldo'] = cur.fetchone()[0]


#created by Bram
def getInformationSponsor(requestEmail):
    cur.execute(
        """select nama from sion.PENGGUNA where sion.PENGGUNA.email = {}""".format(
            "'" + requestEmail + "'"))
    session['nama'] = cur.fetchone()[0]
    cur.execute(
        """select alamat_lengkap from sion.PENGGUNA where sion.PENGGUNA.email = {}""".format(
            "'" + requestEmail + "'"))
    session['alamat'] = cur.fetchone()[0]
    #cur.execute(
    #    """select saldo from sion.SPONSOR where sion.SPONSOR.email = {}""".format(
    #        "'" + requestEmail + "'"))
    #session['saldo'] = cur.fetchone()[0]
    cur.execute(
        """select logo_sponsor from sion.SPONSOR where sion.SPONSOR.email = {}""".format(
            "'" + requestEmail + "'"))
    session['logo'] = cur.fetchone()[0]

#created by Bram
def getInformationPengurus(requestEmail):
    cur.execute(
        """select nama from sion.PENGGUNA where sion.PENGGUNA.email = {}""".format(
            "'" + requestEmail + "'"))
    session['nama'] = cur.fetchone()[0]
    cur.execute(
        """select alamat_lengkap from sion.PENGGUNA where sion.PENGGUNA.email = {}""".format(
            "'" + requestEmail + "'"))
    session['alamat'] = cur.fetchone()[0]
    cur.execute(
        """select nama from sion.organisasi, sion.pengurus_organisasi where sion.pengurus_organisasi.organisasi = sion.organisasi.email_organisasi and sion.pengurus_organisasi.email = {}""".format(
            "'" + requestEmail + "'"))
    session['organisasi'] = cur.fetchone()[0]

#created by Bram
@app.route('/profile')
def profile():
    if session.get('logged_in'):
        role = session['role']
        if role == "relawan":
            getInformationRelawan(session['email'])
            return render_template('profile-relawan.html', alamat=session['alamat'],
                                    nama=session['nama'], email=session['email'],
                                    tanggal_lahir=session['tanggal_lahir'],
                                    no_hp=session['no_hp'], keahlian=session['keahlian'])
        elif role == "donatur":
            getInformationDonatur(session['email'])
            return render_template('profile-donatur.html', nama=session['nama'],
                                    email=session['email'], alamat=session['alamat'],
                                    saldo=session['saldo'])
        elif role == "sponsor":
            getInformationSponsor(session['email'])
            return render_template('profile-sponsor.html', nama=session['nama'],
                                    email=session['email'], alamat=session['alamat'], #saldo=session['saldo'],
                                    logo=session['logo'])
        elif role == "pengurus organisasi":
            getInformationPengurus(session['email'])
            return render_template('profile-pengurus.html', nama=session['nama'],
                                    email=session['email'], alamat=session['alamat'],
                                    organisasi=session['organisasi'])
    else:
        return loginPage(wrongPassword=False, notExist=False)

# register page controller by Arga G. A.
# provide register choices
@app.route('/register')
def registerPage():
    return render_template('register.html')


# register relawan page controller by Arga G. A.
# provide register relawan page
@app.route('/register-relawan', defaults={'exist': False})
def registerRelawanPage(exist):
    return render_template('register-relawan.html', exist=exist)


# register donatur page controller by Arga G. A.
# provide register donatur page
@app.route('/register-donatur', defaults={'exist': False})
def registerDonaturPage(exist):
    return render_template('register-donatur.html', exist=exist)


# register sponsor page controller by Arga G. A.
# provide register sponsor page
@app.route('/register-sponsor', defaults={'exist': False})
def registerSponsorPage(exist):
    return render_template('register-sponsor.html', exist=exist)


# created by Arga G. A.
# method to handle request post of register relawan
@app.route('/register-relawan', methods=['POST'])
def registerRelawan():
    nama = request.form["nama"]
    email = request.form["email"]
    password = request.form["password"]

    if not isPenggunaExists(email):
        kecamatan = request.form["kecamatan"]
        kabupaten = request.form["kabupaten"]
        provinsi = request.form["provinsi"]
        kodepos = request.form["kode-pos"]
        jalan = request.form["jalan"]
        alamat_lengkap = jalan + ", " + kecamatan + ", " + kabupaten + ", " + provinsi + ", " + kodepos

        birthdate = '/'.join(reversed(request.form["tanggal-lahir"].split('-')))
        nomorHandphone = request.form["nomor-handphone"]
        skills = request.form["skills"]

        # print(nama + " " + email + " " + password)
        # print(kecamatan + " " + kabupaten + " " + provinsi + " " + kodepos + " " + jalan)
        # print(birthdate + " " + nomorHandphone + " " + skill)

        cur.execute(
            """INSERT INTO SION.PENGGUNA (email, password, nama, alamat_lengkap) VALUES ({}, {}, {}, {})""".format(
                "'" + email + "'",
                "'" + password + "'",
                "'" + nama + "'",
                "'" + alamat_lengkap + "'"))
        cur.execute(
            """INSERT INTO SION.RELAWAN (email, no_hp, tanggal_lahir) VALUES ({}, {}, {})""".format("'" + email + "'",
                                                                                                    "'" + nomorHandphone + "'",
                                                                                                    "'" + birthdate + "'"))

        listSkills = skills.split(", ")
        for skill in listSkills:
            cur.execute(
                """INSERT INTO SION.KEAHLIAN_RELAWAN (email, keahlian) VALUES ({}, {})""".format("'" + email + "'",
                                                                                                 "'" + skill + "'"))

        session['email'] = email
        session['name'] = nama
        session['role'] = 'relawan'
        session['relawan'] = True
        session['logged_in'] = True

        print("Relawan berhasil dimasukkan!")
        return dashboard(recentlyRegistered=True)
    else:
        return registerRelawanPage(exist=True)


# created by Arga G. A.
# method to handle request post of register donatur
@app.route('/register-donatur', methods=['POST'])
def registerDonatur():
    nama = request.form["nama"]
    email = request.form["email"]
    password = request.form["password"]

    if not isPenggunaExists(email):
        kecamatan = request.form["kecamatan"]
        kabupaten = request.form["kabupaten"]
        provinsi = request.form["provinsi"]
        kodepos = request.form["kode-pos"]
        jalan = request.form["jalan"]
        alamat_lengkap = jalan + ", " + kecamatan + ", " + kabupaten + ", " + provinsi + ", " + kodepos

        # print(nama + " " + email + " " + password)
        # print(kecamatan + " " + kabupaten + " " + provinsi + " " + kodepos + " " + jalan)

        cur.execute(
            """INSERT INTO SION.PENGGUNA (email, password, nama, alamat_lengkap) VALUES ({}, {}, {}, {})""".format(
                "'" + email + "'",
                "'" + password + "'",
                "'" + nama + "'",
                "'" + alamat_lengkap + "'"))
        cur.execute("""INSERT INTO SION.DONATUR (email, saldo) VALUES ({}, 0)""".format("'" + email + "'"))

        session['email'] = email
        session['name'] = nama
        session['role'] = 'donatur'
        session['donatur'] = True
        session['logged_in'] = True

        print("Donatur berhasil dimasukkan!")
        return dashboard(recentlyRegistered=True)
    else:
        return registerDonaturPage(exist=True)


# created by Arga G. A.
# method to handle request post of register sponsor
@app.route('/register-sponsor', methods=['POST'])
def registerSponsor():
    nama = request.form["nama"]
    email = request.form["email"]
    password = request.form["password"]

    if not isPenggunaExists(email):
        kecamatan = request.form["kecamatan"]
        kabupaten = request.form["kabupaten"]
        provinsi = request.form["provinsi"]
        kodepos = request.form["kode-pos"]
        jalan = request.form["jalan"]
        alamat_lengkap = jalan + ", " + kecamatan + ", " + kabupaten + ", " + provinsi + ", " + kodepos

        logo = request.form["logo"]

        # print(nama + " " + email + " " + password)
        # print(kecamatan + " " + kabupaten + " " + provinsi + " " + kodepos + " " + jalan)
        # print(logo)

        cur.execute(
            """INSERT INTO SION.PENGGUNA (email, password, nama, alamat_lengkap) VALUES ({}, {}, {}, {})""".format(
                "'" + email + "'",
                "'" + password + "'",
                "'" + nama + "'",
                "'" + alamat_lengkap + "'"))
        cur.execute("""INSERT INTO SION.SPONSOR (email, logo_sponsor) VALUES ({}, {})""".format("'" + email + "'",
                                                                                                "'" + logo + "'"))

        session['email'] = email
        session['name'] = nama
        session['role'] = 'sponsor'
        session['sponsor'] = True
        session['logged_in'] = True

        print("Sponsor berhasil dimasukkan!")
        return dashboard(recentlyRegistered=True)
    else:
        return registerSponsorPage(exist=True)


# created by Arga G. A.
# method is pengguna exist?
def isPenggunaExists(email):
    cur.execute("""SELECT * FROM SION.PENGGUNA WHERE email = {}""".format("'" + email + "'"))
    user = cur.fetchone()
    if user:
        return True
    else:
        return False

def isOrganisasiExists(email):
    cur.execute("""SELECT * FROM SION.ORGANISASI WHERE email_organisasi = {}""".format("'" + email + "'"))
    organization = cur.fetchone()
    if organization:
        return True
    else:
        return False

#created by Bram
@app.route('/register-organisasi', defaults={'exist': False})
def registerOrganisasiPage(exist):
    return render_template('register-organisasi.html', exist=exist)

#created by Bram
@app.route('/register-organisasi', methods=['POST'])
def registerOrganisasi():
    nama_organisasi = request.form["nama-organisasi"]
    email_organisasi = request.form["email-organisasi"]
    nama_pengurus = request.form["nama-pengurus"]
    email_pengurus = request.form["email-pengurus"]
    website = request.form["website"]

    if (not isPenggunaExists(email_pengurus)) and (not isOrganisasiExists(email_organisasi)):
        kecamatan = request.form["kecamatan"]
        kabupaten = request.form["kabupaten"]
        provinsi = request.form["provinsi"]
        kodepos = request.form["kode-pos"]
        jalan = request.form["jalan"]

        # print(nama + " " + email + " " + password)
        # print(kecamatan + " " + kabupaten + " " + provinsi + " " + kodepos + " " + jalan)

        cur.execute(
            """INSERT INTO SION.ORGANISASI (email_organisasi, website, nama, provinsi, kabupaten_kota, kecamatan, kelurahan, kode_pos, status_verifikasi) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, aktif)""".format(
                "'" + email_organisasi + "'",
                "'" + website + "'",
                "'" + nama_organisasi + "'",
                "'" + provinsi + "'",
                "'" + kabupaten + "'",
                "'" + kecamatan + "'",
                "'" + jalan + "'",
                "'" + kodepos + "'",
                ))
        cur.execute("""INSERT INTO SION.DONATUR (email, saldo) VALUES ({}, 0)""".format("'" + email + "'"))

        session['email'] = email
        session['name'] = nama
        session['role'] = 'donatur'
        session['donatur'] = True
        session['logged_in'] = True

        print("Organisasi berhasil dimasukkan!")
        return dashboard(recentlyRegistered=True)
    else:
        return registerOrganisasiPage(exist=True)

# templating
# read
@app.template_filter('autoversion')
def autoversion_filter(filename):
    # determining fullpath might be project specific
    fullpath = os.path.join('some_app/', filename[1:])
    try:
        timestamp = str(os.path.getmtime(fullpath))
    except OSError:
        return filename
    newfilename = "{0}?v={1}".format(filename, timestamp)
    return newfilename


# main method to run the web server
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.config.update(
        DEBUG=True,
        TEMPLATES_AUTO_RELOAD=True,
    )
    app.run(host='152.118.25.3', port=8101)
