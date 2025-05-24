from flask import Flask, render_template, redirect, url_for, jsonify, request, make_response
import psycopg2
from script2 import mypassword, secret_key, secret_jwt_key
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, current_user

app = Flask(__name__)
uri = f'postgresql://postgres:{mypassword}@localhost/e-commerce'

app.config['SECRET_KEY'] = secret_key
app.config["JWT_SECRET_KEY"] = secret_jwt_key
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
jwt = JWTManager(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

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

    return jsonify({'message':'information was illustrated correctly'})


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return jsonify({'message':'something went wrong'})

        user = Users.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({'message': 'something went wrong'})

        access_token = create_access_token(identity=username)
        return jsonify({'message':'Login success', 'access_token':access_token})
    return jsonify({'message':'something went wrong'})

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        if not username or not password or not email:
            return jsonify({'message': 'something went wrong'})

        hashed_password = generate_password_hash(password)
        new_user = Users(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return jsonify({'message':'something went wrong'})


# create db with images
# create a platform to choose the products
# have an ability to see info about the product
# have an ability to add the product into the basket

# Current problems: payment how it will be done
# Add login/registration form. I do not really know what to use

if __name__ == "__main__":
    app.run(debug=True)