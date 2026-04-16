import mysql.connector
from flask import Flask
from config import Config

app = Flask(__name__, template_folder='views/templates', static_folder='static')
app.config.from_object(Config)

from controllers.auth_controller import init_controller
auth_bp = init_controller(app)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    print("Acesse: http://localhost:8000/login")
    app.run(debug=True, host='0.0.0.0', port=8000)
