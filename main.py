from flask import Flask, render_template, redirect, url_for, jsonify, request
import psycopg2
from script2 import mypassword, secret_key
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

app = Flask(__name__)
uri = f'postgresql://postgres:{mypassword}@localhost/e-commerce'

app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

@app.route('/')
def home():
    conn = psycopg2.connect(host="localhost", dbname="e-commerce", user="postgres",
                            password=mypassword, port=5432)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM products""")
    products = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    return render_template('home.html', products = products)

# create db with images
# create a platform to choose the products
# have an ability to see info about the product
# have an ability to add the product into the basket

# Current problems: payment how it will be done
# Add login/registration form. I do not really know what to use

if __name__ == "__main__":
    app.run(debug=True)