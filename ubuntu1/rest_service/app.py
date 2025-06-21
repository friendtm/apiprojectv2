from flask import Flask
from routes.auth_routes import auth_bp
from routes.esteroides_routes import esteroides_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(esteroides_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
