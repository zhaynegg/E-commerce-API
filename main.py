from flask import Flask
import psycopg2
from script2 import mypassword
app = Flask(__name__)

# create db with images
# create a platform to choose the products
# have an ability to see info about the product
# have an ability to add the product into the basket

# Current problems: payment how it will be done
# Add login/registration form. I do not really know what to use

if __name__ == "__main__":
    app.run(debug=True)