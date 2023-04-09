from flask import Flask, g, request
from flask_cors import CORS
from db_management import get_conn, execute_query
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, uuid, datetime

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = "7177691679bb45cb8cbf88a353497170"

def get_db():
    db = getattr(g, '_database', None)
    if not db:
        db = g._database = get_conn()
    return db

def generate_response(data, status=200):
        if isinstance(data, str):
            return {
                "data" if status < 400 else "error": {
                    "code": status,
                    "message": data
                }
            }, status
        else:
            return {
                "data": data
            }, status
    
def account_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get("x-access-token")
        if not token:
            return generate_response("Account required!", 401)
        try:
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user = execute_query(get_conn(), "SELECT id, username, permission FROM users WHERE public_key=?", (decoded["public_key"],))
            if not user:
                return generate_response("Invalid token!", 401)
        except:
            return generate_response("Invalid token!", 401)
        return f({"id": user[0][0], "username": user[0][1], "permission": user[0][2]}, *args, **kwargs)
    return decorator
    

# API routes

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password") or len(data.get("username")) > 31 or len(data.get("password")) < 6:
        return generate_response("Invalid built username or password!", 400)
    if execute_query(get_conn(), "SELECT id FROM users WHERE username=?", data.get("username")):
        return generate_response("Username already exists!", 409)
    
    execute_query(get_conn(), "INSERT INTO users (public_key, username, password, permission) VALUES (?, ?, ?, ?)",
                   (str(uuid.uuid4()), data.get("username"), generate_password_hash(data.get("password")), 0))
    return generate_response("Registered successfully", 201)

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return generate_response("Username or password missing!", 400)
    
    user = execute_query(get_conn(), "SELECT password, public_key FROM users WHERE username=?", (data.get("username"),))
    if not user or not check_password_hash(user[0][0], data.get("password")):
        return generate_response("Invalid username or password!", 403)
    token = jwt.encode({
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=6),
        "public_key": user[0][1]
        }, app.config["SECRET_KEY"], "HS256")
    return generate_response({"token": token}, 201)

@app.route("/api/account")
@account_required
def account(user):
    return generate_response(user, 200)

@app.route("/api/delete")
@account_required
def delete(user):
    execute_query(get_conn(), "DELETE FROM users WHERE id=?", (user.get("id")))
    return generate_response(user, 200)

if __name__ == "__main__":
    app.run(debug=True)