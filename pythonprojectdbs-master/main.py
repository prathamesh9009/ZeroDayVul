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

if __name__ == "__main__":
    app.run()
