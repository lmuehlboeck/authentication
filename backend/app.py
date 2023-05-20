from flask import Flask, g, request, make_response
from flask_cors import CORS
from db_management import get_conn, execute_query
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, uuid, datetime, os.path

SECRET_KEY_PATH = "./key.txt"
ACCESS_TOKEN_EXP_MIN = 10
REFRESH_TOKEN_EXP_MIN = 600

app = Flask(__name__)
CORS(app, supports_credentials=True)

if not os.path.isfile(SECRET_KEY_PATH):
    with open(SECRET_KEY_PATH, "w+") as f:
        f.write(uuid.uuid4().hex)
with open(SECRET_KEY_PATH, "r") as f:
    app.config['SECRET_KEY'] = f.readline()

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
            user = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            if not user or "id" not in user or "username" not in user or "role" not in user:
                return generate_response("Invalid token!", 401)
        except:
            return generate_response("Invalid token!", 401)
        return f(user, *args, **kwargs)
    return decorator
    

# API routes

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password") or len(data.get("username")) > 30 or len(data.get("password")) < 6:
        return generate_response("Invalid built username or password!", 400)
    if execute_query(get_conn(), "SELECT id FROM users WHERE username=?", (data.get("username"),)):
        return generate_response("Username already exists!", 409)
    
    execute_query(get_conn(), "INSERT INTO users (username, password, role) VALUES (?, ?, 0)",
                   (data.get("username"), generate_password_hash(data.get("password"))))
    return generate_response("Registered successfully", 201)

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return generate_response("Username or password missing!", 400)
    
    user = execute_query(get_conn(), "SELECT id, username, password, role FROM users WHERE username=?", (data.get("username"),))
    if not user or not check_password_hash(user[0][2], data.get("password")):
        return generate_response("Invalid username or password!", 401)
    if user[0][3] < 0:
        return generate_response("Account blocked!", 403)
    access_token = jwt.encode({
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXP_MIN),
        "id": user[0][0],
        "username": user[0][1],
        "role": user[0][3]
        }, app.config["SECRET_KEY"], "HS256")
    refresh_token = jwt.encode({
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=REFRESH_TOKEN_EXP_MIN),
        "id": user[0][0]
    }, app.config["SECRET_KEY"], "HS256")
    resp = make_response(generate_response({"access_token": access_token}, 201))
    resp.set_cookie("refresh_token", refresh_token, httponly=True, path="/api/refresh", samesite="None", secure=True)
    return resp

@app.route("/api/refresh", methods=["PUT"])
def refresh():
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        return generate_response("Refresh token missing!", 400)
    
    try:
        refresh_data = jwt.decode(refresh_token, app.config['SECRET_KEY'], algorithms=['HS256'])
        if not refresh_data and "id" not in refresh_data:
            return generate_response("Invalid refresh token!", 401)
    except:
        return generate_response("Invalid refresh token!", 401)
    user = execute_query(get_conn(), "SELECT id, username, password, role FROM users WHERE id=?", (refresh_data.get("id"),))
    if not user or user[0][3] < 0:
        return generate_response("User blocked or deleted!", 403)
    access_token = jwt.encode({
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXP_MIN),
        "id": user[0][0],
        "username": user[0][1],
        "role": user[0][3]
        }, app.config["SECRET_KEY"], "HS256")
    return generate_response({"access_token": access_token}, 201)
    
@app.route("/api/logout", methods=["DELETE"])
@account_required
def logout(user):
    resp = make_response(generate_response("Logged out successfully!"))
    resp.set_cookie("refresh_token", expires=0, httponly=True, path="/api/refresh", samesite="None", secure=True)
    return resp

@app.route("/api/check", methods=["GET"])
@account_required
def check(user):
    return generate_response(user, 200)

@app.route("/api/delete", methods=["DELETE"])
@account_required
def delete(user):
    execute_query(get_conn(), "DELETE FROM users WHERE id=?", (user.get("id"),))
    resp = make_response(generate_response(user, 200))
    resp.set_cookie("refresh_token", expires=0, httponly=True, path="/api/refresh", samesite="None", secure=True)
    return resp

if __name__ == "__main__":
    app.run(debug=True)