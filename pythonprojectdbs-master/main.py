import email
from flask import Flask, render_template, request, redirect, url_for, send_from_directory 
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

# Redirection from login to reverseshell
@app.route('/rev')
def rev():
    return render_template('rev.html')

@app.route('/redirect_rev', methods=['POST'])
def redirect_to_rev():
    return redirect(url_for('rev'))


@app.route("/user_successful_registration")
def user_successful_registration():
    return render_template('reg.html')

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

@app.route("/user_login_auth")
def user_login_auth():
    return render_template('rev.html')

@app.route("/user_login_fail")
def user_login_fail():
    return render_template('error.html')

#Login connectivity
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form['username']
        password = request.form['password']

        # Query the database for the user's credentials
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        users = cur.fetchone()

        if users:
            # User is authenticated, redirect to the rev.html page
            return redirect(url_for('user_login_auth'))
        else:
            # Authentication failed, redirect to the error.html page
            return redirect(url_for('user_login_fail'))
        
    else:
        # Handle GET request for displaying the login form
        return render_template('index.html')

# Serve script.js
@app.route('/static/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/thank')
def thank():
    return render_template('thank.html')

#Contact form Connection
@app.route('/cont', methods=['GET', 'POST'])
def cont():
    # Check if the form has been submitted
    if request.method == 'POST':
        # Get the form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Connect to the database
        conn = psycopg2.connect(
            host="localhost",
            dbname="zerovuldb",
            user="admin",
            password="root"
        )
        cur = conn.cursor()
        cur.execute("INSERT INTO contactinfo (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
        conn.commit()
        cur.close()
        conn.close()

        # Redirect to a thank-you page
        return redirect(url_for('thank'))
    else:
        # If the form hasn't been submitted, render the contact page
        return render_template('contact.html')
    
@app.route('/ind')
def ind():
    return render_template('index.html')

@app.route('/signin')
def signin():
    return redirect(url_for('ind'))

#Redirection from indexpage navbar to contacts
@app.route("/contact")
def contact():
    return redirect(url_for("contact_page"))

@app.route("/contact_page")
def contact_page():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run()
