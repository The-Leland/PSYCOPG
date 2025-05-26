


from flask import Flask
from db import init_db
from db import create_tables

from routes.companies_routes import companies_bp
from routes.categories_routes import categories_bp
from routes.products_routes import products_bp
from routes.warranties_routes import warranties_bp

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

init_db()

app.register_blueprint(companies_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(products_bp)
app.register_blueprint(warranties_bp)

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

