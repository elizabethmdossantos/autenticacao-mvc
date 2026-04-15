from flask import Flask
from flask_mysqldb import MySQL
from config import Config

app = Flask(
    __name__,
    template_folder='views/templates',
    static_folder='static'
)

app.config.from_object(Config)

mysql = MySQL(app)

from controllers.auth_controller import init_controller
auth_bp = init_controller(mysql)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)