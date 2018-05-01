import os
import psycopg2
from flask import Flask, render_template
import urllib.parse
from os.path import exists
from os import makedirs

# connect for deployed application at heroku
# url = urlparse.urlparse(os.environ.get('DATABASE_URL'))
# db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
# schema = "schema.sql"
# conn = psycopg2.connect(db)

# connect to local database
dbname = ''     #database name
username = ''   #username
password = ''   #password

conn_string = "host='localhost' dbname=%s user=%s password=%s " % (dbname, username, password)
conn = psycopg2.connect(conn_string)

cur = conn.cursor()

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Sistem Informasi Organisasi Nirlaba (SION). Sistem informasi untuk pendaftaran organisasi nirlaba yang dikelola oleh masyarakat sekaligus sebagai media bagi organisasi untuk mengampanyekan kegiatan-kegiatannya.'


@app.route('/users-email')
def getUsersEmail():
    try:
        cur.execute("""SELECT email from sion.pengguna""")
        rows = cur.fetchall()
        my_list = []
        for row in rows:
            my_list.append(row[0])

        return render_template('usersEmail.html', results=my_list)
    except Exception as e:
        print("Ada kesalahan pada method getUsersEmail(), " + e)
        return "Ada kesalahan pada fungsi getUsersEmail."


if __name__ == '__main__':
    app.run()
