import email
from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# database connection
conn = psycopg2.connect(
    host="localhost",
    dbname="zerovuldb",
    user="admin",
    password="root"
)
#Homepage
@app.route("/")
def home():
    return render_template("Homepage.html")

#Redirection from Homepage to indexpage
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/redirect', methods=['POST'])
def redirect_to_index():
    return redirect(url_for('index'))

#Redirection from indexpage to all the tabs in navbar
@app.route('/homepage')
def homepage():
    return render_template('Homepage.html')

@app.route('/redirect', methods=['GET'])
def redirect_to_homepage():
    return redirect(url_for('homepage'))

#Redirection from indexpage navbar to affilate
@app.route('/affliate')
def affliate():
    return render_template('affliate.html')

@app.route('/redirect_affliate', methods=['POST'])
def redirect_to_affliate_handler():
    return redirect(url_for('affliate'))

#Redirection from indexpage navbar to contacts
@app.route('/email')
def email():
    return render_template('email.html')

@app.route('/redirect', methods=['POST'])
def redirect_to_email():
    return redirect(url_for('email'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/redirect', methods=['POST'])
def redirect_to_contact():
    return redirect(url_for('contact'))

@app.route("/user_successful_registration")
def user_successful_registration():
    return render_template('reg.html')

#Redirection from login to Reverseshell
@app.route('/rev')
def rev():
    return render_template('rev.html')

@app.route('/redirect', methods=['POST'])
def redirect_to_rev():
    return redirect(url_for('rev'))

# registration page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # get form data
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # save data to database
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username,email,password) VALUES (%s,%s,%s)", (username,email, password))
        conn.commit()
        cur.close()

        return redirect(url_for('user_successful_registration'))

    return render_template("reg.html")

#Login connectivity
@app.route('/index', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form['username']
        password = request.form['password']

        # Query the database for the user's credentials
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()

        if user:
            # User is authenticated, redirect to the rev.html page
            return redirect('/rev.html')
        else:
            # Authentication failed, redirect to the error.html page
            return redirect('/error.html')
    else:
        return redirect('/index.html')

if __name__ == "__main__":
    app.run()
