from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from routes.users import Users, Register, Login
from config import Config
from routes.videos import Videos
from routes.videos import Comments
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="static")
api = Api(app)
CORS(app)

# Register endpoints
api.add_resource(Users, "/users")  # For retrieving all users
api.add_resource(Register, "/users/register")  # For registering a user
api.add_resource(Login, "/users/login")  # For logging in a user

api.add_resource(Videos, "/videos/upload")

api.add_resource(Comments, "/comments/upload")

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/")
def home():
    return send_from_directory("static", "login.html")