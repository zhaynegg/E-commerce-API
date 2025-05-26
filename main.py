from flask import Flask, render_template, redirect, url_for, jsonify, request, make_response
import psycopg2
from script2 import mypassword, secret_key, secret_jwt_key
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, current_user, get_jwt

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


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Users.query.filter_by(username=identity).one_or_none()


# All about shopping
@app.route('/shopping', methods=['POST', 'GET'])
@jwt_required()
def home():
    conn = psycopg2.connect(host="localhost", dbname="e-commerce", user="postgres",
                            password=mypassword, port=5432)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM products""")
    products = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'information was illustrated correctly', 'products': products})

@app.route('/shopping/<int:id>', methods=['POST', 'GET'])
@jwt_required()
def product_representation(id):
    conn = psycopg2.connect(host="localhost", dbname="e-commerce", user="postgres",
                            password=mypassword, port=5432)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM products WHERE id = %s""" % (id, ))
    products = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()

    if not products:
        return {'msg':'The product does not exist'}

    return jsonify(products)

@app.route('/add_to_basket', methods= ['POST', 'GET'])
@jwt_required()
def add_to_basket():
    data = request.get_json()
    product_id = data.get("product_id")
    count = data.get("count")
    user_id = current_user.id

    if not product_id:
        return {'error': 'There is nothing to add'}

    conn = psycopg2.connect(host="localhost", dbname="e-commerce", user="postgres",
                            password=mypassword, port=5432)
    cur = conn.cursor()
    cur.execute(f"""INSERT INTO baskets(user_id, product_id, count)
                VALUES ({user_id}, {product_id}, {count});""")
    conn.commit()
    cur.close()
    conn.close()
    return {'msg': 'Everything went right'}

@app.route('/my_basket', methods= ['GET', 'POST'])
@jwt_required()
def show_my_basket():
    conn = psycopg2.connect(host="localhost", dbname="e-commerce", user="postgres",
                            password=mypassword, port=5432)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM baskets WHERE user_id = %s""" % (current_user.id,))
    products = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(products)

# Login/Registration
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        # username = request.form.get("username")
        # password = request.form.get("password")

        # getting json
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({'error': 'Password or username is empty'})

        user = Users.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({'error': 'User does not exist or password is incorrect'})

        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token})
    return jsonify({'error': 'Something went wrong'})


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        # form-data
        # username = request.form.get("username")
        # password = request.form.get("password")
        # email = request.form.get("email")

        # getting json
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not password or not email:
            return jsonify({'message': 'Password, Username or email is empty'})

        user = Users.query.filter_by(username=username).first()
        if user:
            return jsonify({'error': 'User already exists'})

        hashed_password = generate_password_hash(password)
        new_user = Users(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Registration was done'})
    return jsonify({'message': 'something went wrong'})


# Current problems: payment how it will be done

if __name__ == "__main__":
    app.run(debug=True)
