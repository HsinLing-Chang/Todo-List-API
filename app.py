from flask import Flask
from routes import user_bp
from routes import task_bp

app = Flask(__name__)
# connect to the blueprint
app.register_blueprint(user_bp)
app.register_blueprint(task_bp)


if __name__ == "__main__":
    print("Server is running on port 8080...")
    app.run(debug=True, port=8080)
